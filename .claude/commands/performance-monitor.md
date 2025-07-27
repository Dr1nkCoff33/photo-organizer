# Performance Monitor Command

## Command: `/performance`

### Description
Performance monitoring and analysis for the photo organizer project.

### Usage
```
/performance [action] [options]
```

### Actions
- `monitor`: Real-time performance monitoring
- `analyze`: Analyze performance of recent operations
- `benchmark`: Run performance benchmarks
- `profile`: Profile code performance
- `optimize`: Suggest performance optimizations
- `report`: Generate performance report
- `history`: Show performance history
- `compare`: Compare performance between versions

### Parameters
- `--duration=time`: Monitoring duration (e.g., 5m, 1h)
- `--interval=time`: Monitoring interval (e.g., 10s, 1m)
- `--output=path`: Output directory for reports
- `--format=type`: Report format (json, csv, html)
- `--threshold=value`: Performance threshold for alerts
- `--memory`: Include memory usage analysis
- `--cpu`: Include CPU usage analysis
- `--disk`: Include disk I/O analysis

### Examples
```
/performance monitor --duration=10m --interval=30s
/performance analyze --output=output/performance
/performance benchmark --format=html
/performance profile --memory --cpu
/performance optimize --threshold=5s
/performance report --format=json
```

### Workflow
1. **Action Selection** - Determine performance operation
2. **Setup Monitoring** - Configure monitoring parameters
3. **Data Collection** - Gather performance metrics
4. **Analysis** - Process and analyze performance data
5. **Reporting** - Generate performance reports
6. **Recommendations** - Provide optimization suggestions

### Output
- Real-time performance metrics
- Performance analysis reports
- Benchmark results and comparisons
- Optimization recommendations
- Performance trends and patterns
- Resource usage statistics
- Bottleneck identification
- Performance improvement suggestions 