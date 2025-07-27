"""
EXIF utility functions for photo organizer
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_exif_data(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Get comprehensive EXIF data using exiftool
    
    Args:
        filepath: Path to photo file
    
    Returns:
        EXIF data dictionary or None if error
    """
    try:
        result = subprocess.run(
            ['exiftool', '-j', str(filepath)], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
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

def extract_capture_date(exif_data: Dict[str, Any]) -> Optional[datetime]:
    """
    Extract capture date from EXIF data
    
    Args:
        exif_data: EXIF data dictionary
    
    Returns:
        Capture date as datetime object or None
    """
    date_fields = [
        'DateTimeOriginal',
        'CreateDate', 
        'ModifyDate',
        'FileModifyDate'
    ]
    
    for field in date_fields:
        if field in exif_data:
            try:
                date_str = exif_data[field]
                # Handle different date formats
                if ':' in date_str:
                    # Format: 2024:01:15 14:30:25
                    date_str = date_str.replace(':', '-', 2)
                return datetime.fromisoformat(date_str.replace(' ', 'T'))
            except (ValueError, TypeError):
                continue
    
    return None

def extract_camera_info(exif_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract camera information from EXIF data
    
    Args:
        exif_data: EXIF data dictionary
    
    Returns:
        Camera information dictionary
    """
    camera_info = {}
    
    # Camera make and model
    camera_info['make'] = exif_data.get('Make', 'Unknown')
    camera_info['model'] = exif_data.get('Model', 'Unknown')
    
    # Lens information
    camera_info['lens'] = exif_data.get('LensModel', 'Unknown')
    camera_info['focal_length'] = exif_data.get('FocalLength', 0)
    camera_info['focal_length_35mm'] = exif_data.get('FocalLengthIn35mmFormat', 0)
    
    # Exposure settings
    camera_info['f_number'] = exif_data.get('FNumber', 0)
    camera_info['iso'] = exif_data.get('ISO', 0)
    camera_info['exposure_time'] = exif_data.get('ExposureTime', 0)
    camera_info['shutter_speed'] = exif_data.get('ShutterSpeed', 0)
    
    return camera_info

def extract_location_info(exif_data: Dict[str, Any]) -> Optional[Dict[str, float]]:
    """
    Extract GPS location information from EXIF data
    
    Args:
        exif_data: EXIF data dictionary
    
    Returns:
        Location dictionary with lat/lon or None
    """
    gps_lat = exif_data.get('GPSLatitude')
    gps_lon = exif_data.get('GPSLongitude')
    
    if gps_lat is not None and gps_lon is not None:
        return {
            'latitude': float(gps_lat),
            'longitude': float(gps_lon)
        }
    
    return None

def get_exif_summary(exif_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of key EXIF information
    
    Args:
        exif_data: EXIF data dictionary
    
    Returns:
        Summary dictionary
    """
    summary = {
        'capture_date': extract_capture_date(exif_data),
        'camera_info': extract_camera_info(exif_data),
        'location': extract_location_info(exif_data),
        'file_size': exif_data.get('FileSize', 0),
        'image_width': exif_data.get('ImageWidth', 0),
        'image_height': exif_data.get('ImageHeight', 0),
        'orientation': exif_data.get('Orientation', 1)
    }
    
    return summary 