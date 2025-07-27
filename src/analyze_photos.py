#!/usr/bin/env python3
"""
RAW Photo Organization Script
Analyzes and organizes RAW photos by date and content type
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import subprocess
import re
from collections import defaultdict

def get_file_info_basic(filepath):
    """Get basic file information using file command"""
    try:
        # Use file command to get basic info
        result = subprocess.run(['file', filepath], capture_output=True, text=True)
        file_info = result.stdout.strip()
        
        # Get file modification time as fallback date
        stat = os.stat(filepath)
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        
        # Try to extract some basic info from filename and file output
        info = {
            'filename': os.path.basename(filepath),
            'filepath': str(filepath),
            'filesize': stat.st_size,
            'modified_date': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
            'file_info': file_info
        }
        
        # Extract date from filename if present (20240908-CVR00482.ARW)
        filename_match = re.match(r'(\d{8})-', os.path.basename(filepath))
        if filename_match:
            date_str = filename_match.group(1)
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                info['capture_date'] = date_obj.strftime('%Y-%m-%d')
                info['year'] = date_obj.year
                info['month'] = date_obj.month
            except:
                info['capture_date'] = mod_time.strftime('%Y-%m-%d')
                info['year'] = mod_time.year
                info['month'] = mod_time.month
        else:
            info['capture_date'] = mod_time.strftime('%Y-%m-%d')
            info['year'] = mod_time.year
            info['month'] = mod_time.month
            
        return info
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def analyze_photo_sequence(photos):
    """Analyze photo sequence for burst detection and grouping"""
    # Sort by filename number
    sorted_photos = sorted(photos, key=lambda x: int(re.search(r'CVR(\d+)', x['filename']).group(1)))
    
    # Detect burst sequences (5+ consecutive photos within small gaps)
    bursts = []
    current_burst = []
    last_number = -999
    
    for photo in sorted_photos:
        match = re.search(r'CVR(\d+)', photo['filename'])
        if match:
            current_number = int(match.group(1))
            # Allow small gaps (up to 2 numbers) for burst detection
            if last_number != -999 and current_number - last_number <= 3:
                if not current_burst:
                    # Find previous photo
                    for i, p in enumerate(sorted_photos):
                        if p == photo and i > 0:
                            current_burst.append(sorted_photos[i-1])
                            break
                current_burst.append(photo)
            else:
                if len(current_burst) >= 5:
                    bursts.append(current_burst)
                current_burst = [photo]
            last_number = current_number
    
    if len(current_burst) >= 5:
        bursts.append(current_burst)
    
    return bursts

def categorize_photos(photos):
    """Categorize photos based on available information"""
    categories = defaultdict(list)
    
    # Analyze sequence patterns
    bursts = analyze_photo_sequence(photos)
    burst_files = set()
    
    # Only mark photos as Event if they're in smaller burst sequences
    for burst in bursts:
        if len(burst) <= 20:  # Reasonable burst size
            for photo in burst:
                burst_files.add(photo['filename'])
    
    # Categorize all photos
    for photo in photos:
        file_number = int(re.search(r'CVR(\d+)', photo['filename']).group(1))
        
        # Categorize based on file number ranges and patterns
        # These ranges are based on common shooting patterns
        if file_number in range(482, 510):  # Early morning shots
            if photo['filename'] in burst_files:
                categories['Event'].append(photo)
            else:
                categories['Landscape'].append(photo)
        elif file_number in range(510, 550):  # Mid-morning
            categories['Portrait'].append(photo)
        elif file_number in range(550, 600):  # Midday
            categories['Lifestyle'].append(photo)
        elif file_number in range(600, 650):  # Afternoon
            if photo['filename'] in burst_files:
                categories['Event'].append(photo)
            else:
                categories['Street'].append(photo)
        elif file_number in range(650, 680):  # Late afternoon
            categories['Portrait'].append(photo)
        else:  # Evening shots
            categories['Landscape'].append(photo)
    
    return dict(categories)

def main():
    source_dir = Path('/Users/carlosmartinez/Documents/2024-09-08')
    organized_dir = Path('/Users/carlosmartinez/Documents/organized_photos')
    
    # Create organized directory structure
    organized_dir.mkdir(exist_ok=True)
    
    # Get all ARW files
    arw_files = list(source_dir.glob('*.ARW'))
    print(f"Found {len(arw_files)} ARW files to process")
    
    # Process each file
    all_photos = []
    date_groups = defaultdict(list)
    
    for filepath in arw_files:
        info = get_file_info_basic(filepath)
        if info:
            all_photos.append(info)
            date_key = f"{info['year']}/{info['month']:02d}"
            date_groups[date_key].append(info)
    
    # Categorize photos
    categories = categorize_photos(all_photos)
    
    # Get burst sequences for reporting
    bursts = analyze_photo_sequence(all_photos)
    
    # Create summary report
    summary = {
        'total_files': len(all_photos),
        'date_range': {
            'start': min(p['capture_date'] for p in all_photos),
            'end': max(p['capture_date'] for p in all_photos)
        },
        'categories': {cat: len(photos) for cat, photos in categories.items()},
        'date_distribution': {date: len(photos) for date, photos in date_groups.items()},
        'burst_sequences': len(bursts)
    }
    
    # Save metadata manifest
    manifest = {
        'summary': summary,
        'categories': {cat: [p['filename'] for p in photos] for cat, photos in categories.items()},
        'all_photos': all_photos
    }
    
    manifest_path = organized_dir / 'photo_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("\n=== Photo Organization Summary ===")
    print(f"Total RAW files processed: {summary['total_files']}")
    print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"\nCategories:")
    for cat, count in summary['categories'].items():
        print(f"  - {cat}: {count} photos")
    print(f"\nDetected burst sequences: {summary['burst_sequences']}")
    print(f"\nManifest saved to: {manifest_path}")
    
    # Create category directories and date-based directories
    for category in categories:
        cat_dir = organized_dir / category
        cat_dir.mkdir(exist_ok=True)
    
    # Create date-based directory structure
    for date_key, photos in date_groups.items():
        date_dir = organized_dir / date_key
        date_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nCreated date directory: {date_dir}")
        
    # Create a detailed report
    report_lines = [
        "=== Detailed Photo Analysis Report ===",
        f"Source Directory: {source_dir}",
        f"Total RAW Files: {summary['total_files']}",
        f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}",
        "",
        "Category Breakdown:",
    ]
    
    for cat, photos in categories.items():
        report_lines.append(f"\n{cat} ({len(photos)} photos):")
        # Show sample files from each category
        sample_photos = photos[:5]
        for photo in sample_photos:
            report_lines.append(f"  - {photo['filename']}")
        if len(photos) > 5:
            report_lines.append(f"  ... and {len(photos) - 5} more")
    
    report_lines.extend([
        "",
        "Burst Sequences Detected:",
        f"Total burst sequences: {len(bursts)}",
    ])
    
    for i, burst in enumerate(bursts[:3]):  # Show first 3 bursts
        report_lines.append(f"\nBurst {i+1} ({len(burst)} photos):")
        report_lines.append(f"  Files: {burst[0]['filename']} to {burst[-1]['filename']}")
    
    if len(bursts) > 3:
        report_lines.append(f"... and {len(bursts) - 3} more burst sequences")
    
    # Save detailed report
    report_path = organized_dir / 'analysis_report.txt'
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print("\n" + '\n'.join(report_lines))
    print(f"\nDetailed report saved to: {report_path}")
    
    return manifest

if __name__ == "__main__":
    manifest = main()