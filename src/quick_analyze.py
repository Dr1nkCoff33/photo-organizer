#!/usr/bin/env python3
"""
Quick Photo Analysis Tool
Simplified interface for fast photo categorization
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .analyze_photos_exif import main as enhanced_analyzer, PhotoAnalyzerConfig
from .claude_analyzer import ClaudePhotoAnalyzer

def quick_analyze(source_dir: str, 
                 output_dir: Optional[str] = None,
                 config_path: Optional[str] = None,
                 use_claude: bool = False,
                 organize: bool = False) -> None:
    """Quick analysis with minimal output"""
    
    # Always prompt for output directory if not provided
    if output_dir is None:
        print("\n📂 Where should I save the analysis results?")
        print("   (Enter full path to output directory)")
        output_path = input("   Output directory: ").strip()
        if not output_path:
            print("❌ Output directory is required")
            sys.exit(1)
        output_dir = Path(output_path)
    else:
        output_dir = Path(output_dir)
    
    print(f"📸 Quick Photo Analysis")
    print(f"📁 Source: {source_dir}")
    print(f"📂 Output: {output_dir}")
    print(f"🤖 Claude AI: {'Enabled' if use_claude else 'Disabled'}")
    print(f"📦 Organize: {'Yes' if organize else 'No'}")
    print("-" * 50)
    
    # Run analysis
    try:
        result = enhanced_analyzer(
            source_dir=source_dir,
            output_dir=str(output_dir),
            config_path=config_path,
            organize=organize,
            move_files=False
        )
        
        if result:
            summary = result['summary']
            print(f"\n✅ Analysis Complete!")
            print(f"📊 Total Photos: {summary['total_files']}")
            
            # Show top categories
            categories = summary['analyzed_categories']
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            
            print(f"\n📈 Top Categories:")
            for category, count in sorted_cats[:5]:
                percentage = (count / summary['total_files']) * 100
                print(f"  {category:<12} {count:>3} ({percentage:>5.1f}%)")
            
            if summary.get('burst_sequences', 0) > 0:
                print(f"\n🎯 Burst Sequences: {summary['burst_sequences']}")
            
            print(f"\n📄 Results saved to: {output_dir}")
            
        else:
            print("❌ Analysis failed or no results returned")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Quick Photo Analysis - Fast categorization with minimal output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick analysis
  python -m src.quick_analyze /path/to/photos

  # With Claude AI
  python -m src.quick_analyze /path/to/photos --claude

  # With custom config and organization
  python -m src.quick_analyze /path/to/photos --config config/enhanced.yaml --organize
        """
    )
    
    parser.add_argument('source_dir', help='Directory containing photos to analyze')
    parser.add_argument('--output-dir', help='Output directory (default: analysis_output)')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--claude', action='store_true', help='Enable Claude AI analysis')
    parser.add_argument('--organize', action='store_true', help='Organize photos after analysis')
    
    args = parser.parse_args()
    
    # Validate source directory
    source_path = Path(args.source_dir)
    if not source_path.exists():
        print(f"❌ Source directory does not exist: {source_path}")
        sys.exit(1)
    
    # Set Claude API key if requested
    if args.claude and not ClaudePhotoAnalyzer().enabled:
        print("⚠️  Claude AI requested but API key not found.")
        print("   Set CLAUDE_API_KEY environment variable or use --no-claude")
        sys.exit(1)
    
    # Run quick analysis
    quick_analyze(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        config_path=args.config,
        use_claude=args.claude,
        organize=args.organize
    )

if __name__ == '__main__':
    main() 