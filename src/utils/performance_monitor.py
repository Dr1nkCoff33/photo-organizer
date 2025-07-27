#!/usr/bin/env python3
"""
Performance Monitor for Photo Organizer
Provides real-time monitoring, analysis, and benchmarking capabilities
"""

import os
import sys
import time
import json
import psutil
import threading
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict, deque
from contextlib import contextmanager
import logging
import signal
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_pdf import PdfPages

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Container for performance metrics"""
    
    def __init__(self):
        self.cpu_percent = 0.0
        self.memory_info = {}
        self.disk_io = {}
        self.process_metrics = {}
        self.operation_timings = defaultdict(list)
        self.timestamps = []
        self.custom_metrics = {}


class PerformanceMonitor:
    """Real-time performance monitoring for photo organizer"""
    
    def __init__(self, interval: float = 1.0, history_size: int = 3600):
        self.interval = interval
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.current_metrics = PerformanceMetrics()
        self.monitoring = False
        self.monitor_thread = None
        self.process = psutil.Process()
        self.start_time = time.time()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 70.0,
            'disk_usage_percent': 90.0,
            'response_time': 5.0
        }
        
        # Alert callbacks
        self.alert_callbacks = []
        
    def start(self):
        """Start monitoring in background thread"""
        if self.monitoring:
            logger.warning("Monitoring is already running")
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
        
    def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=self.interval * 2)
        logger.info("Performance monitoring stopped")
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                self._collect_metrics()
                self._check_thresholds()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                
    def _collect_metrics(self):
        """Collect current performance metrics"""
        metrics = PerformanceMetrics()
        
        # CPU metrics
        metrics.cpu_percent = self.process.cpu_percent(interval=0.1)
        
        # Memory metrics
        memory = self.process.memory_info()
        metrics.memory_info = {
            'rss': memory.rss,
            'vms': memory.vms,
            'percent': self.process.memory_percent(),
            'available': psutil.virtual_memory().available
        }
        
        # Disk I/O metrics
        try:
            io_counters = self.process.io_counters()
            metrics.disk_io = {
                'read_bytes': io_counters.read_bytes,
                'write_bytes': io_counters.write_bytes,
                'read_count': io_counters.read_count,
                'write_count': io_counters.write_count
            }
        except (AttributeError, psutil.AccessDenied):
            metrics.disk_io = {}
            
        # Process-specific metrics
        metrics.process_metrics = {
            'num_threads': self.process.num_threads(),
            'num_fds': self.process.num_fds() if hasattr(self.process, 'num_fds') else 0,
            'status': self.process.status(),
            'create_time': self.process.create_time()
        }
        
        # Timestamp
        metrics.timestamps = datetime.now()
        
        # Store metrics
        self.current_metrics = metrics
        self.metrics_history.append(metrics)
        
    def _check_thresholds(self):
        """Check if any metrics exceed thresholds"""
        alerts = []
        
        if self.current_metrics.cpu_percent > self.thresholds['cpu_percent']:
            alerts.append(f"High CPU usage: {self.current_metrics.cpu_percent:.1f}%")
            
        if self.current_metrics.memory_info.get('percent', 0) > self.thresholds['memory_percent']:
            alerts.append(f"High memory usage: {self.current_metrics.memory_info['percent']:.1f}%")
            
        for alert in alerts:
            logger.warning(alert)
            for callback in self.alert_callbacks:
                callback(alert)
                
    @contextmanager
    def measure_operation(self, operation_name: str):
        """Context manager to measure operation timing"""
        start_time = time.time()
        start_memory = self.process.memory_info().rss
        
        yield
        
        end_time = time.time()
        end_memory = self.process.memory_info().rss
        
        duration = end_time - start_time
        memory_delta = end_memory - start_memory
        
        self.current_metrics.operation_timings[operation_name].append({
            'duration': duration,
            'memory_delta': memory_delta,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Operation '{operation_name}' took {duration:.3f}s, memory delta: {memory_delta / 1024 / 1024:.1f}MB")
        
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {}
            
        cpu_values = [m.cpu_percent for m in self.metrics_history]
        memory_values = [m.memory_info.get('percent', 0) for m in self.metrics_history]
        
        summary = {
            'monitoring_duration': time.time() - self.start_time,
            'samples_collected': len(self.metrics_history),
            'cpu': {
                'current': self.current_metrics.cpu_percent,
                'average': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            },
            'memory': {
                'current_mb': self.current_metrics.memory_info.get('rss', 0) / 1024 / 1024,
                'current_percent': self.current_metrics.memory_info.get('percent', 0),
                'average_percent': sum(memory_values) / len(memory_values),
                'max_percent': max(memory_values)
            },
            'operation_timings': {}
        }
        
        # Add operation timing summaries
        for op_name, timings in self.current_metrics.operation_timings.items():
            if timings:
                durations = [t['duration'] for t in timings]
                summary['operation_timings'][op_name] = {
                    'count': len(timings),
                    'total': sum(durations),
                    'average': sum(durations) / len(durations),
                    'max': max(durations),
                    'min': min(durations)
                }
                
        return summary
        
    def export_metrics(self, output_path: Path, format: str = 'json'):
        """Export collected metrics"""
        data = {
            'summary': self.get_summary(),
            'history': [
                {
                    'timestamp': m.timestamps.isoformat() if hasattr(m.timestamps, 'isoformat') else str(m.timestamps),
                    'cpu_percent': m.cpu_percent,
                    'memory_mb': m.memory_info.get('rss', 0) / 1024 / 1024,
                    'memory_percent': m.memory_info.get('percent', 0),
                    'disk_read_mb': m.disk_io.get('read_bytes', 0) / 1024 / 1024,
                    'disk_write_mb': m.disk_io.get('write_bytes', 0) / 1024 / 1024
                }
                for m in list(self.metrics_history)
            ]
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == 'csv':
            df = pd.DataFrame(data['history'])
            df.to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        logger.info(f"Metrics exported to {output_path}")


class PerformanceBenchmark:
    """Benchmarking utilities for photo organizer"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.benchmarks = {}
        
    def benchmark_operation(self, operation: Callable, name: str, iterations: int = 10) -> Dict[str, Any]:
        """Benchmark a specific operation"""
        timings = []
        memory_usage = []
        
        for i in range(iterations):
            with self.monitor.measure_operation(f"benchmark_{name}_{i}"):
                start_memory = self.monitor.process.memory_info().rss
                start_time = time.time()
                
                operation()
                
                end_time = time.time()
                end_memory = self.monitor.process.memory_info().rss
                
                timings.append(end_time - start_time)
                memory_usage.append(end_memory - start_memory)
                
        result = {
            'name': name,
            'iterations': iterations,
            'timing': {
                'average': sum(timings) / len(timings),
                'min': min(timings),
                'max': max(timings),
                'total': sum(timings)
            },
            'memory': {
                'average_delta_mb': sum(memory_usage) / len(memory_usage) / 1024 / 1024,
                'max_delta_mb': max(memory_usage) / 1024 / 1024
            }
        }
        
        self.benchmarks[name] = result
        return result
        
    def compare_operations(self, operations: Dict[str, Callable], iterations: int = 10):
        """Compare performance of multiple operations"""
        results = {}
        
        for name, operation in operations.items():
            logger.info(f"Benchmarking {name}...")
            results[name] = self.benchmark_operation(operation, name, iterations)
            
        return results
        
    def generate_report(self, output_path: Path):
        """Generate benchmark report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024,
                'platform': sys.platform
            },
            'benchmarks': self.benchmarks
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Benchmark report saved to {output_path}")


class PerformanceAnalyzer:
    """Analyze performance data and generate insights"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        
    def analyze_bottlenecks(self) -> Dict[str, Any]:
        """Identify performance bottlenecks"""
        summary = self.monitor.get_summary()
        bottlenecks = []
        
        # CPU bottleneck
        if summary.get('cpu', {}).get('average', 0) > 70:
            bottlenecks.append({
                'type': 'cpu',
                'severity': 'high' if summary['cpu']['average'] > 90 else 'medium',
                'description': f"High CPU usage: {summary['cpu']['average']:.1f}% average"
            })
            
        # Memory bottleneck
        if summary.get('memory', {}).get('average_percent', 0) > 60:
            bottlenecks.append({
                'type': 'memory',
                'severity': 'high' if summary['memory']['average_percent'] > 80 else 'medium',
                'description': f"High memory usage: {summary['memory']['average_percent']:.1f}% average"
            })
            
        # Slow operations
        for op_name, timing in summary.get('operation_timings', {}).items():
            if timing['average'] > 1.0:
                bottlenecks.append({
                    'type': 'operation',
                    'severity': 'high' if timing['average'] > 5.0 else 'medium',
                    'description': f"Slow operation '{op_name}': {timing['average']:.2f}s average",
                    'details': timing
                })
                
        return {
            'bottlenecks': bottlenecks,
            'recommendations': self._generate_recommendations(bottlenecks)
        }
        
    def _generate_recommendations(self, bottlenecks: List[Dict]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        for bottleneck in bottlenecks:
            if bottleneck['type'] == 'cpu':
                recommendations.extend([
                    "Consider using more efficient algorithms",
                    "Increase parallel processing batch size",
                    "Profile CPU-intensive operations"
                ])
            elif bottleneck['type'] == 'memory':
                recommendations.extend([
                    "Implement better caching strategies",
                    "Process files in smaller batches",
                    "Clear unused caches periodically"
                ])
            elif bottleneck['type'] == 'operation':
                recommendations.extend([
                    f"Optimize '{bottleneck['description'].split("'")[1]}' operation",
                    "Consider caching results",
                    "Use batch processing where possible"
                ])
                
        return list(set(recommendations))  # Remove duplicates
        
    def generate_visualization(self, output_path: Path):
        """Generate performance visualization"""
        if not self.monitor.metrics_history:
            logger.warning("No metrics to visualize")
            return
            
        # Prepare data
        timestamps = []
        cpu_values = []
        memory_values = []
        
        for metrics in self.monitor.metrics_history:
            timestamps.append(metrics.timestamps)
            cpu_values.append(metrics.cpu_percent)
            memory_values.append(metrics.memory_info.get('percent', 0))
            
        # Create plots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # CPU usage plot
        ax1.plot(timestamps, cpu_values, 'b-', label='CPU %')
        ax1.axhline(y=self.monitor.thresholds['cpu_percent'], color='r', linestyle='--', label='Threshold')
        ax1.set_ylabel('CPU Usage (%)')
        ax1.set_title('CPU Usage Over Time')
        ax1.legend()
        ax1.grid(True)
        
        # Memory usage plot
        ax2.plot(timestamps, memory_values, 'g-', label='Memory %')
        ax2.axhline(y=self.monitor.thresholds['memory_percent'], color='r', linestyle='--', label='Threshold')
        ax2.set_ylabel('Memory Usage (%)')
        ax2.set_xlabel('Time')
        ax2.set_title('Memory Usage Over Time')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Performance visualization saved to {output_path}")


def main():
    """Main entry point for performance monitor"""
    parser = argparse.ArgumentParser(description='Performance Monitor for Photo Organizer')
    parser.add_argument('action', choices=['monitor', 'analyze', 'benchmark', 'report'],
                       help='Action to perform')
    parser.add_argument('--duration', type=str, default='5m',
                       help='Monitoring duration (e.g., 5m, 1h)')
    parser.add_argument('--interval', type=float, default=1.0,
                       help='Monitoring interval in seconds')
    parser.add_argument('--output', type=str, default='output/performance',
                       help='Output directory for reports')
    parser.add_argument('--format', choices=['json', 'csv', 'html'], default='json',
                       help='Report format')
    parser.add_argument('--threshold', type=float,
                       help='Performance threshold for alerts')
    
    args = parser.parse_args()
    
    # Parse duration
    duration_str = args.duration
    if duration_str.endswith('m'):
        duration = float(duration_str[:-1]) * 60
    elif duration_str.endswith('h'):
        duration = float(duration_str[:-1]) * 3600
    else:
        duration = float(duration_str)
        
    # Create monitor
    monitor = PerformanceMonitor(interval=args.interval)
    
    if args.threshold:
        monitor.thresholds['response_time'] = args.threshold
        
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.action == 'monitor':
        # Start monitoring
        monitor.start()
        logger.info(f"Monitoring for {duration}s...")
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            logger.info("Monitoring interrupted by user")
            
        monitor.stop()
        
        # Export results
        monitor.export_metrics(output_dir / f'metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{args.format}', 
                             format=args.format)
                             
    elif args.action == 'analyze':
        # Analyze existing metrics
        analyzer = PerformanceAnalyzer(monitor)
        
        # Load metrics if available
        # TODO: Implement loading from previous runs
        
        analysis = analyzer.analyze_bottlenecks()
        
        with open(output_dir / 'analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
            
        analyzer.generate_visualization(output_dir / 'performance_plot.png')
        
    elif args.action == 'benchmark':
        # Run benchmarks
        benchmark = PerformanceBenchmark(monitor)
        
        # TODO: Add specific photo processing benchmarks
        
        benchmark.generate_report(output_dir / 'benchmark_report.json')
        
    elif args.action == 'report':
        # Generate comprehensive report
        monitor.start()
        time.sleep(10)  # Collect some data
        monitor.stop()
        
        summary = monitor.get_summary()
        
        with open(output_dir / 'performance_report.json', 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"Performance report saved to {output_dir / 'performance_report.json'}")


if __name__ == '__main__':
    main()