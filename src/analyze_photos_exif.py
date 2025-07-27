#!/usr/bin/env python3
"""
Enhanced RAW Photo Organization Script with EXIF Analysis
Uses exiftool to analyze metadata and properly categorize photos
Optimized for performance with parallel processing, caching, and batch operations
"""

import os
import json
import shutil
import pickle
import yaml
from datetime import datetime
from pathlib import Path
import subprocess
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from typing import Dict, List, Optional, Tuple, Any
import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhotoAnalyzerConfig:
    """Configuration management for photo analyzer"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        default_config = {
            'max_workers': None,  # Will be set to CPU count + 4
            'batch_size': 50,
            'cache_enabled': True,
            'cache_dir': None,  # Will be set to ~/.photo_analyzer_cache
            'progress_file': None,
            'categories': {
                'Portrait': {'focal_range': (50, 135), 'f_number_max': 2.8, 'weight': 1.0},
                'Landscape': {'focal_range': (0, 35), 'f_number_min': 8, 'weight': 1.0},
                'Street': {'focal_range': (28, 50), 'weight': 1.0},
                'Event': {'burst_threshold': 5, 'weight': 1.0},
                'Wildlife': {'focal_range': (200, 999), 'weight': 1.0},
                'Sports': {'focal_range': (200, 999), 'weight': 1.0},
                'Macro': {'subject_distance_max': 50, 'weight': 1.0},
                'Architecture': {'focal_range': (0, 24), 'weight': 1.0},
                'Night': {'iso_min': 1600, 'weight': 1.0}
            }
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        # Set default values if not provided
        if default_config['max_workers'] is None:
            default_config['max_workers'] = min(32, (os.cpu_count() or 1) + 4)
        
        if default_config['cache_dir'] is None:
            default_config['cache_dir'] = str(Path.home() / '.photo_analyzer_cache')
        
        return default_config

def get_exif_data(filepath: Path) -> Optional[Dict[str, Any]]:
    """Get comprehensive EXIF data using exiftool"""
    try:
        result = subprocess.run(['exiftool', '-j', str(filepath)], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            exif_data = json.loads(result.stdout)[0]
            return exif_data
        else:
            logger.warning(f"Error reading EXIF data from {filepath}: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout reading EXIF data from {filepath}")
        return None
    except Exception as e:
        logger.error(f"Error processing {filepath}: {e}")
        return None

def get_exif_data_cached(filepath: Path, cache_dir: Path) -> Optional[Dict[str, Any]]:
    """Get EXIF data with caching to avoid re-processing"""
    cache_file = cache_dir / f"{filepath.stem}_exif.pkl"
    
    # Check if cached data exists and is newer than file
    if cache_file.exists() and cache_file.stat().st_mtime > filepath.stat().st_mtime:
        try:
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
                logger.debug(f"Using cached EXIF data for {filepath}")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load cached data for {filepath}: {e}")
    
    # Get fresh EXIF data
    exif_data = get_exif_data(filepath)
    if exif_data:
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(exif_data, f)
            logger.debug(f"Cached EXIF data for {filepath}")
        except Exception as e:
            logger.warning(f"Failed to cache EXIF data for {filepath}: {e}")
    
    return exif_data

def get_exif_data_batch(filepaths: List[Path], batch_size: int = 50) -> List[Tuple[Path, Dict[str, Any]]]:
    """Process multiple files in batches using exiftool for better performance"""
    results = []
    
    for i in range(0, len(filepaths), batch_size):
        batch = filepaths[i:i + batch_size]
        try:
            result = subprocess.run(
                ['exiftool', '-j'] + [str(f) for f in batch],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                batch_data = json.loads(result.stdout)
                for j, exif_data in enumerate(batch_data):
                    if exif_data:  # Skip empty results
                        results.append((batch[j], exif_data))
            else:
                logger.warning(f"Error processing batch: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.warning(f"Timeout processing batch of {len(batch)} files")
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
    
    return results

def process_files_parallel(filepaths: List[Path], config: PhotoAnalyzerConfig) -> List[Tuple[Path, Dict[str, Any]]]:
    """Process multiple files concurrently for better performance"""
    cache_dir = Path(config.config['cache_dir'])
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    with ThreadPoolExecutor(max_workers=config.config['max_workers']) as executor:
        if config.config['cache_enabled']:
            # Use cached version for individual files
            future_to_file = {
                executor.submit(get_exif_data_cached, filepath, cache_dir): filepath 
                for filepath in filepaths
            }
        else:
            # Use batch processing for better performance
            future_to_file = {
                executor.submit(get_exif_data_batch, filepaths[i:i + config.config['batch_size']], config.config['batch_size']): i
                for i in range(0, len(filepaths), config.config['batch_size'])
            }
        
        for future in tqdm.tqdm(as_completed(future_to_file), 
                              total=len(future_to_file), 
                              desc="Processing EXIF data"):
            try:
                if config.config['cache_enabled']:
                    filepath = future_to_file[future]
                    exif_data = future.result()
                    if exif_data:
                        results.append((filepath, exif_data))
                else:
                    batch_results = future.result()
                    results.extend(batch_results)
            except Exception as e:
                logger.error(f"Error in parallel processing: {e}")
    
    return results

def process_with_progress(filepaths: List[Path], config: PhotoAnalyzerConfig) -> List[Tuple[Path, Dict[str, Any]]]:
    """Process files with progress tracking and ability to resume interrupted processing"""
    processed = set()
    
    if config.config['progress_file'] and Path(config.config['progress_file']).exists():
        try:
            with open(config.config['progress_file'], 'r') as f:
                processed = set(json.load(f))
            logger.info(f"Resuming from previous run. {len(processed)} files already processed.")
        except Exception as e:
            logger.warning(f"Failed to load progress file: {e}")
    
    remaining = [f for f in filepaths if str(f) not in processed]
    logger.info(f"Processing {len(remaining)} remaining files out of {len(filepaths)} total")
    
    results = []
    for filepath in tqdm.tqdm(remaining, desc="Processing photos"):
        exif_data = get_exif_data_cached(filepath, Path(config.config['cache_dir']))
        if exif_data:
            results.append((filepath, exif_data))
            processed.add(str(filepath))
            
            # Save progress periodically
            if len(results) % 100 == 0 and config.config['progress_file']:
                try:
                    with open(config.config['progress_file'], 'w') as f:
                        json.dump(list(processed), f)
                except Exception as e:
                    logger.warning(f"Failed to save progress: {e}")
    
    return results

def analyze_photo_for_category(exif_data: Dict[str, Any], config: PhotoAnalyzerConfig) -> str:
    """Analyze EXIF data to determine photo category with improved accuracy and context awareness"""
    category_scores = {cat: 0 for cat in config.config['categories'].keys()}
    
    # Extract relevant EXIF fields with better parsing
    focal_length = exif_data.get('FocalLength', '').replace(' mm', '')
    f_number = exif_data.get('FNumber', 0)
    iso = exif_data.get('ISO', 0)
    shutter_speed = exif_data.get('ShutterSpeed', '')
    metering_mode = exif_data.get('MeteringMode', '')
    focus_mode = exif_data.get('FocusMode', '')
    af_area_mode = exif_data.get('AFAreaModeSetting', '')
    scene_mode = exif_data.get('SceneMode', '')
    subject_distance = exif_data.get('SubjectDistance', '')
    lens_model = exif_data.get('LensModel', '') or exif_data.get('LensSpec', '')
    exposure_mode = exif_data.get('ExposureMode', '')
    flash = exif_data.get('Flash', '')
    
    # Convert focal length to float with better error handling
    try:
        focal_length_num = float(focal_length) if focal_length else 0
    except (ValueError, TypeError):
        focal_length_num = 0
    
    # Convert f-number to float
    try:
        f_number_num = float(f_number) if f_number else 0
    except (ValueError, TypeError):
        f_number_num = 0
    
    # Convert ISO to int
    try:
        iso_num = int(iso) if iso else 0
    except (ValueError, TypeError):
        iso_num = 0
    
    # Enhanced Portrait detection with context
    portrait_config = config.config['categories']['Portrait']
    portrait_score = 0
    
    # Primary indicators
    if (portrait_config['focal_range'][0] <= focal_length_num <= portrait_config['focal_range'][1]):
        portrait_score += 4 * portrait_config['weight']
    if f_number_num > 0 and f_number_num <= portrait_config['f_number_max']:
        portrait_score += 3 * portrait_config['weight']
    if 'portrait' in scene_mode.lower():
        portrait_score += 6 * portrait_config['weight']
    
    # Secondary indicators
    if af_area_mode in ['Center', 'Spot', 'Flexible Spot', 'Single Point']:
        portrait_score += 2 * portrait_config['weight']
    if focus_mode in ['AF-S', 'Single AF']:
        portrait_score += 1 * portrait_config['weight']
    if exposure_mode in ['Aperture Priority', 'Manual']:
        portrait_score += 1 * portrait_config['weight']
    
    # Negative indicators (reduce score if present)
    if focal_length_num < 35:  # Too wide for typical portraits
        portrait_score -= 2
    if f_number_num > 8:  # Too narrow aperture
        portrait_score -= 2
    
    category_scores['Portrait'] = max(0, portrait_score)
    
    # Enhanced Landscape detection
    landscape_config = config.config['categories']['Landscape']
    landscape_score = 0
    
    # Primary indicators
    if (landscape_config['focal_range'][0] <= focal_length_num <= landscape_config['focal_range'][1]):
        landscape_score += 4 * landscape_config['weight']
    if f_number_num >= landscape_config['f_number_min']:
        landscape_score += 3 * landscape_config['weight']
    if 'landscape' in scene_mode.lower():
        landscape_score += 6 * landscape_config['weight']
    
    # Secondary indicators
    if af_area_mode in ['Wide', 'Zone', 'Multi']:
        landscape_score += 2 * landscape_config['weight']
    if focus_mode in ['AF-S', 'Manual']:
        landscape_score += 1 * landscape_config['weight']
    if exposure_mode in ['Aperture Priority', 'Manual']:
        landscape_score += 1 * landscape_config['weight']
    
    # Negative indicators
    if focal_length_num > 100:  # Too telephoto for typical landscapes
        landscape_score -= 2
    if f_number_num < 4:  # Too wide aperture
        landscape_score -= 2
    
    category_scores['Landscape'] = max(0, landscape_score)
    
    # Enhanced Street photography detection
    street_config = config.config['categories']['Street']
    street_score = 0
    
    # Primary indicators
    if (street_config['focal_range'][0] <= focal_length_num <= street_config['focal_range'][1]):
        street_score += 3 * street_config['weight']
    if 3.5 <= f_number_num <= 8:
        street_score += 2 * street_config['weight']
    
    # Secondary indicators
    if metering_mode in ['Average', 'Center-weighted average', 'Multi-segment']:
        street_score += 1 * street_config['weight']
    if focus_mode in ['AF-C', 'Continuous AF']:
        street_score += 2 * street_config['weight']
    if exposure_mode in ['Aperture Priority', 'Program']:
        street_score += 1 * street_config['weight']
    if af_area_mode in ['Wide', 'Zone']:
        street_score += 1 * street_config['weight']
    
    # Context indicators
    if iso_num >= 400:  # Higher ISO for low light street
        street_score += 1 * street_config['weight']
    
    category_scores['Street'] = max(0, street_score)
    
    # Enhanced Wildlife/Sports detection
    wildlife_config = config.config['categories']['Wildlife']
    sports_config = config.config['categories']['Sports']
    
    wildlife_score = 0
    sports_score = 0
    
    # Primary indicators
    if (wildlife_config['focal_range'][0] <= focal_length_num <= wildlife_config['focal_range'][1]):
        wildlife_score += 5 * wildlife_config['weight']
        sports_score += 4 * sports_config['weight']
    
    # Secondary indicators
    if focus_mode in ['AF-C', 'Continuous AF']:
        wildlife_score += 2 * wildlife_config['weight']
        sports_score += 3 * sports_config['weight']
    
    # Shutter speed analysis for sports
    if shutter_speed:
        try:
            # Parse shutter speed (e.g., "1/500" -> 0.002)
            if '/' in shutter_speed:
                parts = shutter_speed.split('/')
                if len(parts) == 2:
                    speed = float(parts[0]) / float(parts[1])
                    if speed <= 0.002:  # 1/500 or faster
                        sports_score += 3 * sports_config['weight']
                    elif speed <= 0.01:  # 1/100 or faster
                        sports_score += 1 * sports_config['weight']
        except:
            pass
    
    # Context indicators
    if af_area_mode in ['Zone', 'Wide']:
        wildlife_score += 1 * wildlife_config['weight']
        sports_score += 1 * sports_config['weight']
    
    category_scores['Wildlife'] = max(0, wildlife_score)
    category_scores['Sports'] = max(0, sports_score)
    
    # Enhanced Macro detection
    macro_config = config.config['categories']['Macro']
    macro_score = 0
    
    # Primary indicators
    if 'macro' in lens_model.lower():
        macro_score += 8 * macro_config['weight']
    
    # Subject distance analysis
    if subject_distance and 'cm' in subject_distance:
        try:
            distance = float(subject_distance.replace(' cm', ''))
            if distance < macro_config['subject_distance_max']:
                macro_score += 4 * macro_config['weight']
        except:
            pass
    
    # Secondary indicators
    if f_number_num >= 8:  # Narrow aperture for depth of field
        macro_score += 1 * macro_config['weight']
    if focus_mode in ['AF-S', 'Manual']:
        macro_score += 1 * macro_config['weight']
    
    category_scores['Macro'] = max(0, macro_score)
    
    # Enhanced Night photography detection
    night_config = config.config['categories']['Night']
    night_score = 0
    
    # Primary indicators
    if iso_num >= night_config['iso_min']:
        night_score += 3 * night_config['weight']
    if 'night' in scene_mode.lower():
        night_score += 6 * night_config['weight']
    
    # Secondary indicators
    if iso_num >= 3200:
        night_score += 2 * night_config['weight']
    if f_number_num >= 2.8:  # Wide aperture for low light
        night_score += 1 * night_config['weight']
    if flash and 'No flash' not in flash:
        night_score += 1 * night_config['weight']
    
    category_scores['Night'] = max(0, night_score)
    
    # Enhanced Architecture detection
    arch_config = config.config['categories']['Architecture']
    arch_score = 0
    
    # Primary indicators
    if (arch_config['focal_range'][0] <= focal_length_num <= arch_config['focal_range'][1]):
        arch_score += 3 * arch_config['weight']
    if 5.6 <= f_number_num <= 11:
        arch_score += 2 * arch_config['weight']
    
    # Secondary indicators
    if focus_mode in ['AF-S', 'Manual']:
        arch_score += 1 * arch_config['weight']
    if af_area_mode in ['Center', 'Spot']:
        arch_score += 1 * arch_config['weight']
    if exposure_mode in ['Aperture Priority', 'Manual']:
        arch_score += 1 * arch_config['weight']
    
    category_scores['Architecture'] = max(0, arch_score)
    
    # Event detection (burst sequences will be handled separately)
    event_score = 0
    if exif_data.get('BurstMode'):
        event_score += 3 * config.config['categories']['Event']['weight']
    if exif_data.get('SequenceNumber'):
        event_score += 1 * config.config['categories']['Event']['weight']
    
    category_scores['Event'] = max(0, event_score)
    
    # Find category with highest score and apply confidence threshold
    max_score = max(category_scores.values())
    
    # Apply confidence threshold - require minimum score to avoid false positives
    confidence_threshold = 3.0
    if max_score < confidence_threshold:
        return 'Uncategorized'
    
    # Return category with highest score
    for category, score in category_scores.items():
        if score == max_score:
            return category
    
    return 'Uncategorized'

def analyze_photo_sequence(photos: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Analyze photo sequence for burst detection and grouping"""
    if not photos:
        return []
    
    # Sort by capture time first, then by filename
    sorted_photos = sorted(photos, key=lambda x: (x.get('capture_timestamp', 0), x['filename']))
    
    # Detect burst sequences (photos taken within 1 second of each other)
    bursts = []
    current_burst = []
    last_timestamp = 0
    
    for photo in sorted_photos:
        current_timestamp = photo.get('capture_timestamp', 0)
        
        # If photos are within 1 second, consider them part of a burst
        if last_timestamp != 0 and current_timestamp - last_timestamp <= 1:
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
            current_burst = []
        
        last_timestamp = current_timestamp
    
    if len(current_burst) >= 5:
        bursts.append(current_burst)
    
    return bursts

def process_large_collection(filepaths: List[Path], output_file: Path, config: PhotoAnalyzerConfig):
    """Process large collections without loading everything into memory"""
    logger.info(f"Processing large collection of {len(filepaths)} files")
    
    with open(output_file, 'w') as f:
        f.write('[\n')  # Start JSON array
        
        for i in range(0, len(filepaths), config.config['batch_size']):
            batch = filepaths[i:i + config.config['batch_size']]
            batch_results = process_files_parallel(batch, config)
            
            for j, (filepath, exif_data) in enumerate(batch_results):
                if i > 0 or j > 0:
                    f.write(',\n')
                json.dump({'filepath': str(filepath), 'exif': exif_data}, f)
            
            logger.info(f"Processed batch {i//config.config['batch_size'] + 1}/{(len(filepaths) + config.config['batch_size'] - 1)//config.config['batch_size']}")
        
        f.write('\n]')  # End JSON array

def organize_photos(photos: List[Dict[str, Any]], output_dir: Path, move_files: bool = False) -> Dict[str, int]:
    """Organize photos into folders based on their categories"""
    organized_count = defaultdict(int)
    
    for photo in tqdm.tqdm(photos, desc="Organizing photos"):
        category = photo.get('analyzed_category', 'Uncategorized')
        
        # Create category directory
        category_dir = output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create date-based subdirectory
        if photo.get('year') and photo.get('month'):
            date_subdir = category_dir / f"{photo['year']}-{photo['month']:02d}"
            date_subdir.mkdir(exist_ok=True)
            target_dir = date_subdir
        else:
            target_dir = category_dir
        
        source_path = Path(photo['filepath'])
        target_path = target_dir / source_path.name
        
        try:
            if move_files:
                # Move the file
                if source_path.exists() and not target_path.exists():
                    shutil.move(str(source_path), str(target_path))
                    logger.info(f"Moved {source_path.name} to {target_dir}")
                    organized_count[category] += 1
                elif target_path.exists():
                    logger.warning(f"Target already exists: {target_path}")
            else:
                # Copy the file
                if source_path.exists() and not target_path.exists():
                    shutil.copy2(str(source_path), str(target_path))
                    logger.info(f"Copied {source_path.name} to {target_dir}")
                    organized_count[category] += 1
                elif target_path.exists():
                    logger.warning(f"Target already exists: {target_path}")
        except Exception as e:
            logger.error(f"Error organizing {source_path.name}: {e}")
    
    return dict(organized_count)

def main(source_dir: Optional[str] = None, output_dir: Optional[str] = None, config_path: Optional[str] = None, organize: bool = False, move_files: bool = False):
    """Main function with enhanced performance and configuration
    
    Args:
        source_dir: Directory containing photos to analyze
        output_dir: Directory for output (analysis results and/or organized photos)
        config_path: Path to configuration file
        organize: Whether to organize photos into folders
        move_files: Whether to move (True) or copy (False) files when organizing
    """
    
    # Initialize configuration
    config = PhotoAnalyzerConfig(config_path)
    
    if source_dir is None:
        source_dir = Path('/Users/carlosmartinez/Documents/organized_photos')
    else:
        source_dir = Path(source_dir)
    
    if output_dir is None:
        output_dir = Path('/Users/carlosmartinez/Document/GitHub/photo-organizer/output/exif_analysis')
    else:
        output_dir = Path(output_dir)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all ARW files
    arw_files = list(source_dir.rglob('*.ARW'))
    logger.info(f"Found {len(arw_files)} ARW files to analyze with EXIF data")
    
    if not arw_files:
        logger.warning("No ARW files found in source directory")
        return None
    
    # Process files based on collection size
    if len(arw_files) > 10000:  # Large collection
        logger.info("Large collection detected, using streaming processing")
        temp_file = output_dir / 'temp_exif_data.json'
        process_large_collection(arw_files, temp_file, config)
        
        # Load results for analysis
        with open(temp_file, 'r') as f:
            all_results = json.load(f)
        all_photos = []
        for result in all_results:
            if result['exif']:
                all_photos.append(process_photo_data(Path(result['filepath']), result['exif']))
        
        # Clean up temp file
        temp_file.unlink()
    else:
        # Standard processing for smaller collections
        logger.info("Using standard parallel processing")
        results = process_files_parallel(arw_files, config)
        
        # Process each file
        all_photos = []
        date_groups = defaultdict(list)
        category_distribution = defaultdict(list)
        
        logger.info("Analyzing EXIF data and categorizing photos...")
        for filepath, exif_data in tqdm.tqdm(results, desc="Analyzing photos"):
            photo_info = process_photo_data(filepath, exif_data)
            if photo_info:
                all_photos.append(photo_info)
                
                # Group by date
                if photo_info.get('year') and photo_info.get('month'):
                    date_key = f"{photo_info['year']}/{photo_info['month']:02d}"
                    date_groups[date_key].append(photo_info)
                
                # Determine category based on EXIF analysis
                category = analyze_photo_for_category(exif_data, config)
                photo_info['analyzed_category'] = category
                category_distribution[category].append(photo_info)
    
    # Analyze burst sequences
    bursts = analyze_photo_sequence(all_photos)
    
    # Update Event category for burst photos
    burst_photos = set()
    for burst in bursts:
        for photo in burst:
            burst_photos.add(photo['filename'])
            # Move to Event category if it's a burst
            if photo['analyzed_category'] != 'Event':
                category_distribution[photo['analyzed_category']].remove(photo)
                photo['analyzed_category'] = 'Event'
                category_distribution['Event'].append(photo)
    
    # Optional: Integrate Claude AI analysis for content validation
    try:
        from .claude_analyzer import ClaudePhotoAnalyzer, integrate_claude_analysis
        
        claude_analyzer = ClaudePhotoAnalyzer()
        if claude_analyzer.enabled:
            logger.info("Claude AI analysis enabled - running content validation...")
            all_photos = integrate_claude_analysis(all_photos, claude_analyzer, sample_size=20)
            
            # Recalculate category distribution after Claude analysis
            category_distribution = defaultdict(list)
            for photo in all_photos:
                category_distribution[photo['analyzed_category']].append(photo)
        else:
            logger.info("Claude AI analysis disabled - using EXIF-only categorization")
    except ImportError:
        logger.info("Claude AI module not available - using EXIF-only categorization")
    except Exception as e:
        logger.warning(f"Claude AI analysis failed: {e} - continuing with EXIF-only categorization")
    
    # Create summary report
    summary = {
        'total_files': len(all_photos),
        'date_range': {
            'start': min(p['capture_date'] for p in all_photos if p.get('capture_date')),
            'end': max(p['capture_date'] for p in all_photos if p.get('capture_date'))
        },
        'analyzed_categories': {cat: len(photos) for cat, photos in category_distribution.items()},
        'date_distribution': {date: len(photos) for date, photos in date_groups.items()},
        'burst_sequences': len(bursts),
        'burst_photos': len(burst_photos),
        'processing_stats': {
            'cache_enabled': config.config['cache_enabled'],
            'max_workers': config.config['max_workers'],
            'batch_size': config.config['batch_size']
        }
    }
    
    # Compare current vs analyzed categories
    category_comparison = defaultdict(lambda: defaultdict(int))
    for photo in all_photos:
        current = photo.get('current_category', 'Unknown')
        analyzed = photo['analyzed_category']
        category_comparison[current][analyzed] += 1
    
    # Save detailed analysis
    analysis_data = {
        'summary': summary,
        'category_comparison': dict(category_comparison),
        'sample_mismatches': [],
        'burst_sequences': [[p['filename'] for p in burst] for burst in bursts[:5]]  # First 5 bursts
    }
    
    # Find mismatched categorizations (limited to first 50 for simplicity)
    for photo in all_photos[:50]:
        if photo.get('current_category') and photo['current_category'] != photo['analyzed_category']:
            analysis_data['sample_mismatches'].append({
                'filename': photo['filename'],
                'current_category': photo['current_category'],
                'analyzed_category': photo['analyzed_category'],
                'focal_length': photo.get('focal_length'),
                'f_number': photo.get('f_number'),
                'iso': photo.get('iso'),
                'focus_mode': photo.get('focus_mode'),
                'scene_mode': photo.get('scene_mode')
            })
    
    # Save detailed analysis results
    analysis_path = output_dir / 'exif_analysis_results.json'
    with open(analysis_path, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    # Create simplified reports
    simple_report_path = create_simplified_report(analysis_data, output_dir)
    simple_json_path = create_json_summary(analysis_data, output_dir)
    
    logger.info(f"\n📊 Analysis completed!")
    logger.info(f"📄 Detailed results: {analysis_path}")
    logger.info(f"📋 Summary report: {simple_report_path}")
    logger.info(f"📊 JSON summary: {simple_json_path}")
    
    # Organize photos if requested
    if organize:
        logger.info("\n=== Organizing Photos ===")
        organize_dir = output_dir / 'organized'
        organize_dir.mkdir(exist_ok=True)
        
        organized_count = organize_photos(all_photos, organize_dir, move_files)
        
        logger.info("\nOrganization Summary:")
        for category, count in sorted(organized_count.items()):
            logger.info(f"  - {category}: {count} photos")
        
        total_organized = sum(organized_count.values())
        logger.info(f"\nTotal photos organized: {total_organized}")
        logger.info(f"Photos {'moved' if move_files else 'copied'} to: {organize_dir}")
        
        # Update analysis data with organization results
        analysis_data['organization_results'] = {
            'organized_count': organized_count,
            'total_organized': total_organized,
            'output_directory': str(organize_dir),
            'operation': 'move' if move_files else 'copy'
        }
        
        # Save updated analysis data
        with open(analysis_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
    
    return analysis_data

def process_photo_data(filepath: Path, exif_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process individual photo data from EXIF"""
    try:
        # Extract key metadata
        photo_info = {
            'filename': exif_data.get('FileName'),
            'filepath': str(filepath),
            'filesize': exif_data.get('FileSize'),
            'camera': f"{exif_data.get('Make', '')} {exif_data.get('Model', '')}",
            'lens': exif_data.get('LensModel') or exif_data.get('LensSpec', ''),
            'focal_length': exif_data.get('FocalLength'),
            'f_number': exif_data.get('FNumber'),
            'iso': exif_data.get('ISO'),
            'shutter_speed': exif_data.get('ShutterSpeed'),
            'capture_date': exif_data.get('DateTimeOriginal'),
            'metering_mode': exif_data.get('MeteringMode'),
            'focus_mode': exif_data.get('FocusMode'),
            'af_area_mode': exif_data.get('AFAreaModeSetting'),
            'white_balance': exif_data.get('WhiteBalance'),
            'scene_mode': exif_data.get('SceneMode'),
            'exif_data': exif_data  # Store full EXIF data
        }
        
        # Parse capture timestamp
        try:
            capture_dt = datetime.strptime(exif_data.get('DateTimeOriginal', ''), '%Y:%m:%d %H:%M:%S')
            photo_info['capture_timestamp'] = capture_dt.timestamp()
            photo_info['year'] = capture_dt.year
            photo_info['month'] = capture_dt.month
        except:
            photo_info['capture_timestamp'] = 0
        
        # Get current category from path
        current_category = filepath.parent.name
        if current_category not in ['organized_photos', '2024', '09']:
            photo_info['current_category'] = current_category
        
        return photo_info
    except Exception as e:
        logger.error(f"Error processing photo data for {filepath}: {e}")
        return None

def create_simplified_report(analysis_data: Dict[str, Any], output_dir: Path) -> None:
    """Create a simplified, more readable analysis report"""
    
    summary = analysis_data['summary']
    category_comparison = analysis_data['category_comparison']
    
    # Create simplified report
    report_lines = [
        "📸 PHOTO ANALYSIS SUMMARY",
        "=" * 50,
        f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"📁 Total Photos: {summary['total_files']:,}",
        f"📅 Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}",
        "",
        "📊 CATEGORY BREAKDOWN",
        "-" * 30,
    ]
    
    # Sort categories by count
    sorted_categories = sorted(
        summary['analyzed_categories'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    for category, count in sorted_categories:
        percentage = (count / summary['total_files']) * 100
        report_lines.append(f"  {category:<12} {count:>4} photos ({percentage:>5.1f}%)")
    
    # Add burst information if significant
    if summary.get('burst_sequences', 0) > 0:
        report_lines.extend([
            "",
            "🎯 BURST DETECTION",
            "-" * 30,
            f"  Burst Sequences: {summary['burst_sequences']}",
            f"  Burst Photos: {summary['burst_photos']} ({summary['burst_photos']/summary['total_files']*100:.1f}%)"
        ])
    
    # Add category changes summary
    if category_comparison:
        report_lines.extend([
            "",
            "🔄 CATEGORY CHANGES",
            "-" * 30,
        ])
        
        total_changes = 0
        for current_cat, analyzed_cats in category_comparison.items():
            changes = sum(count for analyzed_cat, count in analyzed_cats.items() 
                         if analyzed_cat != current_cat)
            if changes > 0:
                total_changes += changes
                report_lines.append(f"  {current_cat:<12} → {changes:>3} photos reclassified")
        
        if total_changes > 0:
            change_percentage = (total_changes / summary['total_files']) * 100
            report_lines.append(f"  Total Changes: {total_changes} ({change_percentage:.1f}%)")
        else:
            report_lines.append("  No category changes detected")
    
    # Add processing stats
    if 'processing_stats' in summary:
        stats = summary['processing_stats']
        report_lines.extend([
            "",
            "⚙️ PROCESSING INFO",
            "-" * 30,
            f"  Cache Enabled: {'Yes' if stats.get('cache_enabled') else 'No'}",
            f"  Workers: {stats.get('max_workers', 'N/A')}",
            f"  Batch Size: {stats.get('batch_size', 'N/A')}"
        ])
    
    # Save simplified report
    simple_report_path = output_dir / 'analysis_summary.txt'
    with open(simple_report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    # Also print to console
    print('\n' + '\n'.join(report_lines))
    
    return simple_report_path

def create_json_summary(analysis_data: Dict[str, Any], output_dir: Path) -> None:
    """Create a simplified JSON summary with only essential data"""
    
    summary = analysis_data['summary']
    
    # Create simplified JSON structure
    simple_summary = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_photos": summary['total_files'],
            "date_range": summary['date_range']
        },
        "categories": summary['analyzed_categories'],
        "burst_info": {
            "sequences": summary.get('burst_sequences', 0),
            "photos": summary.get('burst_photos', 0)
        },
        "changes": {
            "total_changes": 0,
            "change_percentage": 0.0
        }
    }
    
    # Calculate changes
    if 'category_comparison' in analysis_data:
        total_changes = 0
        for current_cat, analyzed_cats in analysis_data['category_comparison'].items():
            changes = sum(count for analyzed_cat, count in analyzed_cats.items() 
                         if analyzed_cat != current_cat)
            total_changes += changes
        
        simple_summary["changes"]["total_changes"] = total_changes
        simple_summary["changes"]["change_percentage"] = (total_changes / summary['total_files']) * 100
    
    # Save simplified JSON
    simple_json_path = output_dir / 'analysis_summary.json'
    with open(simple_json_path, 'w') as f:
        json.dump(simple_summary, f, indent=2)
    
    return simple_json_path

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze and organize RAW photos using EXIF data')
    parser.add_argument('source_dir', nargs='?', help='Source directory containing photos')
    parser.add_argument('output_dir', nargs='?', help='Output directory for results and organized photos')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--organize', action='store_true', help='Organize photos into category folders')
    parser.add_argument('--move', action='store_true', help='Move files instead of copying (use with --organize)')
    
    args = parser.parse_args()
    
    main(args.source_dir, args.output_dir, args.config, args.organize, args.move)