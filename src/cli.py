#!/usr/bin/env python3
"""
Command-line interface for Photo Organizer
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .analyze_photos import main as basic_analyzer
from .analyze_photos_exif import main as enhanced_analyzer, PhotoAnalyzerConfig

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Photo Organizer - RAW photo analysis and organization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python -m src.cli analyze /path/to/photos /path/to/output

  # Enhanced EXIF analysis
  python -m src.cli analyze-exif /path/to/photos /path/to/output

  # Use custom configuration
  python -m src.cli analyze-exif /path/to/photos /path/to/output --config config/custom.yaml

  # Organize photos by moving them
  python -m src.cli organize /path/to/photos /path/to/output --move
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Basic analyzer command
    basic_parser = subparsers.add_parser('analyze', help='Basic photo analysis')
    basic_parser.add_argument('source_dir', help='Source directory containing photos')
    basic_parser.add_argument('output_dir', help='Output directory for analysis results')
    basic_parser.add_argument('--file-types', help='Comma-separated list of file extensions')
    basic_parser.add_argument('--organize-by-date', action='store_true', help='Organize photos by date')
    basic_parser.add_argument('--detect-bursts', action='store_true', help='Detect burst sequences')
    
    # Enhanced analyzer command
    enhanced_parser = subparsers.add_parser('analyze-exif', help='Enhanced EXIF analysis')
    enhanced_parser.add_argument('source_dir', help='Source directory containing photos')
    enhanced_parser.add_argument('output_dir', help='Output directory for analysis results')
    enhanced_parser.add_argument('--config', help='Path to configuration file')
    enhanced_parser.add_argument('--organize', action='store_true', help='Organize photos after analysis')
    enhanced_parser.add_argument('--move', action='store_true', help='Move files instead of copying')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize photos by date and category')
    organize_parser.add_argument('source_dir', help='Source directory containing photos')
    organize_parser.add_argument('output_dir', help='Output directory for organized photos')
    organize_parser.add_argument('--move', action='store_true', help='Move files instead of copying')
    organize_parser.add_argument('--config', help='Path to configuration file')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run performance tests')
    test_parser.add_argument('--source-dir', help='Test source directory')
    test_parser.add_argument('--output-dir', help='Test output directory')
    
    return parser

def run_basic_analyzer(args) -> int:
    """Run basic photo analyzer"""
    try:
        source_dir = Path(args.source_dir)
        output_dir = Path(args.output_dir)
        
        if not source_dir.exists():
            print(f"Error: Source directory does not exist: {source_dir}")
            return 1
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert file types string to list if provided
        file_types = None
        if args.file_types:
            file_types = [ext.strip() for ext in args.file_types.split(',')]
        
        print(f"Starting basic analysis of {source_dir}")
        print(f"Output directory: {output_dir}")
        
        # Call the basic analyzer
        result = basic_analyzer()
        
        print("Basic analysis completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error during basic analysis: {e}")
        return 1

def run_enhanced_analyzer(args) -> int:
    """Run enhanced EXIF analyzer"""
    try:
        source_dir = Path(args.source_dir)
        output_dir = Path(args.output_dir)
        config_path = args.config
        
        if not source_dir.exists():
            print(f"Error: Source directory does not exist: {source_dir}")
            return 1
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Starting enhanced EXIF analysis of {source_dir}")
        print(f"Output directory: {output_dir}")
        if config_path:
            print(f"Configuration file: {config_path}")
        
        # Call the enhanced analyzer
        result = enhanced_analyzer(
            source_dir=str(source_dir),
            output_dir=str(output_dir),
            config_path=config_path,
            organize=args.organize,
            move_files=args.move
        )
        
        if result:
            print("Enhanced analysis completed successfully!")
            print(f"Processed {result['summary']['total_files']} files")
            print(f"Found {len(result['summary']['analyzed_categories'])} categories")
        else:
            print("Analysis completed but no results returned")
        
        return 0
        
    except Exception as e:
        print(f"Error during enhanced analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1

def run_organize(args) -> int:
    """Run photo organization"""
    try:
        source_dir = Path(args.source_dir)
        output_dir = Path(args.output_dir)
        config_path = args.config
        
        if not source_dir.exists():
            print(f"Error: Source directory does not exist: {source_dir}")
            return 1
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Organizing photos from {source_dir}")
        print(f"Output directory: {output_dir}")
        print(f"Move files: {args.move}")
        
        # First analyze, then organize
        result = enhanced_analyzer(
            source_dir=str(source_dir),
            output_dir=str(output_dir),
            config_path=config_path,
            organize=True,
            move_files=args.move
        )
        
        if result:
            print("Photo organization completed successfully!")
            print(f"Organized {result['summary']['total_files']} files")
        else:
            print("Organization completed but no results returned")
        
        return 0
        
    except Exception as e:
        print(f"Error during organization: {e}")
        import traceback
        traceback.print_exc()
        return 1

def run_tests(args) -> int:
    """Run performance tests"""
    try:
        from .test_enhanced_analyzer import main as run_test_main
        run_test_main()
        return 0
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main() -> int:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'analyze':
        return run_basic_analyzer(args)
    elif args.command == 'analyze-exif':
        return run_enhanced_analyzer(args)
    elif args.command == 'organize':
        return run_organize(args)
    elif args.command == 'test':
        return run_tests(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 