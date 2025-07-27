#!/usr/bin/env python3
"""
Simple wrapper script to organize photos using EXIF analysis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analyze_photos_exif import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Organize RAW photos by analyzing EXIF metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze and organize photos (copy mode)
  python organize_photos.py /path/to/photos /path/to/output --organize
  
  # Analyze and move photos into organized folders
  python organize_photos.py /path/to/photos /path/to/output --organize --move
  
  # Just analyze without organizing
  python organize_photos.py /path/to/photos /path/to/output
        """
    )
    
    parser.add_argument('source_dir', help='Directory containing RAW photos to organize')
    parser.add_argument('output_dir', help='Output directory for organized photos')
    parser.add_argument('--organize', action='store_true', 
                      help='Actually organize photos into folders (default: just analyze)')
    parser.add_argument('--move', action='store_true', 
                      help='Move files instead of copying them (use with --organize)')
    parser.add_argument('--config', help='Path to configuration YAML file')
    
    args = parser.parse_args()
    
    # Default to organizing if not just analyzing
    if not args.organize:
        print("\n⚠️  Running in ANALYSIS mode only. Photos will NOT be organized.")
        print("   Add --organize flag to actually organize photos into folders.\n")
    
    if args.move and not args.organize:
        print("⚠️  Warning: --move flag has no effect without --organize\n")
    
    # Run the main function
    main(args.source_dir, args.output_dir, args.config, args.organize, args.move)