#!/usr/bin/env python3
"""
Configuration file for Photo Organizer
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Photo file extensions
RAW_EXTENSIONS = {
    '.ARW', '.CR2', '.NEF', '.RAF', '.ORF', '.RW2', 
    '.PEF', '.SRW', '.DNG', '.RAW'
}

IMAGE_EXTENSIONS = {
    '.JPG', '.JPEG', '.PNG', '.TIFF', '.TIF', '.BMP', '.GIF'
}

ALL_PHOTO_EXTENSIONS = RAW_EXTENSIONS | IMAGE_EXTENSIONS

# Analysis settings
BURST_DETECTION_THRESHOLD = 5  # Minimum photos for burst detection
BURST_TIME_WINDOW = 30  # Seconds between photos for burst detection

# Organization settings
DATE_FORMAT = "%Y-%m-%d"
ORGANIZE_BY_DATE = True
DETECT_BURSTS = True
CREATE_CATEGORIES = True

# Output settings
REPORT_FORMAT = "json"  # json, csv, markdown
INCLUDE_METADATA = True
INCLUDE_THUMBNAILS = False

# File naming patterns
FILENAME_PATTERNS = {
    'date_prefix': r'(\d{8})-',  # YYYYMMDD-
    'camera_code': r'CVR(\d+)',  # Camera sequence number
}

# Environment variables
ENV_VARS = {
    'PHOTO_INPUT_DIR': os.getenv('PHOTO_INPUT_DIR', ''),
    'PHOTO_OUTPUT_DIR': os.getenv('PHOTO_OUTPUT_DIR', ''),
    'PHOTO_BACKUP_DIR': os.getenv('PHOTO_BACKUP_DIR', ''),
} 