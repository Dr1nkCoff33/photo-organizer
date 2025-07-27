"""
Date utility functions for photo organizer
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import re

def parse_date_from_filename(filename: str) -> Optional[datetime]:
    """
    Parse date from filename patterns like '20240908-CVR00482.ARW'
    
    Args:
        filename: Filename to parse
    
    Returns:
        Parsed datetime or None
    """
    # Pattern: YYYYMMDD-CVR
    pattern = r'(\d{8})-'
    match = re.search(pattern, filename)
    
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            pass
    
    return None

def format_date_for_directory(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format date for directory naming
    
    Args:
        date: Date to format
        format_str: Format string
    
    Returns:
        Formatted date string
    """
    return date.strftime(format_str)

def group_photos_by_date(photos: List[dict], date_field: str = 'capture_date') -> dict:
    """
    Group photos by date
    
    Args:
        photos: List of photo dictionaries
        date_field: Field name containing the date
    
    Returns:
        Dictionary with dates as keys and photo lists as values
    """
    grouped = {}
    
    for photo in photos:
        if date_field in photo and photo[date_field]:
            if isinstance(photo[date_field], str):
                # Convert string to datetime if needed
                try:
                    date = datetime.fromisoformat(photo[date_field].replace('Z', '+00:00'))
                except ValueError:
                    continue
            else:
                date = photo[date_field]
            
            date_key = date.strftime('%Y-%m-%d')
            if date_key not in grouped:
                grouped[date_key] = []
            grouped[date_key].append(photo)
    
    return grouped

def detect_burst_sequence(photos: List[dict], 
                         time_threshold: int = 30,
                         min_photos: int = 3) -> List[List[dict]]:
    """
    Detect burst sequences based on time proximity
    
    Args:
        photos: List of photo dictionaries
        time_threshold: Time threshold in seconds for burst detection
        min_photos: Minimum number of photos to consider a burst
    
    Returns:
        List of burst sequences (each sequence is a list of photos)
    """
    if not photos:
        return []
    
    # Sort photos by capture date
    sorted_photos = sorted(photos, key=lambda x: x.get('capture_date', datetime.min))
    
    bursts = []
    current_burst = []
    
    for i, photo in enumerate(sorted_photos):
        if 'capture_date' not in photo:
            continue
            
        current_date = photo['capture_date']
        
        if not current_burst:
            current_burst = [photo]
        else:
            # Check time difference with last photo in current burst
            last_date = current_burst[-1]['capture_date']
            time_diff = abs((current_date - last_date).total_seconds())
            
            if time_diff <= time_threshold:
                current_burst.append(photo)
            else:
                # End current burst if it meets minimum criteria
                if len(current_burst) >= min_photos:
                    bursts.append(current_burst)
                current_burst = [photo]
    
    # Don't forget the last burst
    if len(current_burst) >= min_photos:
        bursts.append(current_burst)
    
    return bursts

def get_date_range(photos: List[dict], date_field: str = 'capture_date') -> Optional[Tuple[datetime, datetime]]:
    """
    Get the date range of a photo collection
    
    Args:
        photos: List of photo dictionaries
        date_field: Field name containing the date
    
    Returns:
        Tuple of (earliest_date, latest_date) or None
    """
    dates = []
    
    for photo in photos:
        if date_field in photo and photo[date_field]:
            if isinstance(photo[date_field], str):
                try:
                    date = datetime.fromisoformat(photo[date_field].replace('Z', '+00:00'))
                except ValueError:
                    continue
            else:
                date = photo[date_field]
            dates.append(date)
    
    if dates:
        return (min(dates), max(dates))
    
    return None

def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h" 