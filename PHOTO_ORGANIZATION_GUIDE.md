# Photo Organization Guide

This guide explains how to use the enhanced photo organizer that analyzes EXIF metadata to properly categorize and organize your RAW photos.

## Quick Start

### 1. Basic Organization (Copy Mode)
```bash
python organize_photos.py /path/to/raw/photos /path/to/output --organize
```
This will:
- Analyze all RAW photos using EXIF data
- Categorize them (Portrait, Landscape, Street, Event, etc.)
- Copy photos into organized folders: `Category/YYYY-MM/filename.ARW`

### 2. Move Photos Instead of Copying
```bash
python organize_photos.py /path/to/raw/photos /path/to/output --organize --move
```
⚠️ **Warning**: This will MOVE files from source to destination!

### 3. Analysis Only (No Organization)
```bash
python organize_photos.py /path/to/raw/photos /path/to/output
```
This only analyzes photos and generates reports without moving/copying files.

## Output Structure

After organization, your photos will be structured like:
```
output/
├── organized/
│   ├── Portrait/
│   │   ├── 2024-09/
│   │   │   ├── 20240908-CVR00510.ARW
│   │   │   └── 20240908-CVR00511.ARW
│   │   └── 2024-10/
│   │       └── 20241015-IMG00123.ARW
│   ├── Landscape/
│   │   └── 2024-09/
│   │       ├── 20240908-CVR00482.ARW
│   │       └── 20240908-CVR00483.ARW
│   ├── Event/
│   │   └── 2024-09/
│   │       └── [burst sequences]
│   └── Street/
│       └── 2024-09/
│           └── 20240908-CVR00600.ARW
├── exif_analysis_results.json
└── exif_analysis_report.txt
```

## Categories

Photos are categorized based on EXIF metadata analysis:

- **Portrait**: 50-135mm focal length, wide aperture (f/2.8 or wider)
- **Landscape**: Wide angle (<35mm), small aperture (f/8+)
- **Street**: 28-50mm focal length, continuous AF mode
- **Event**: Burst sequences (5+ photos within 1 second)
- **Wildlife/Sports**: Telephoto (200mm+), fast shutter speeds
- **Macro**: Macro lens detected or very close subject distance
- **Architecture**: Ultra-wide (<24mm), f/8-11
- **Night**: High ISO (1600+)

## Advanced Usage

### Custom Configuration
Create a `config.yaml` file:
```yaml
max_workers: 16
batch_size: 100
cache_enabled: true
categories:
  Portrait:
    focal_range: [85, 200]  # Include 85-200mm for portraits
    f_number_max: 4.0
    weight: 1.5  # Increase weight for portrait detection
```

Use with:
```bash
python organize_photos.py /input /output --organize --config config.yaml
```

### Large Collections (10,000+ photos)
The script automatically switches to streaming mode for large collections to avoid memory issues.

## Important Notes

1. **Requires exiftool**: Make sure exiftool is installed (`brew install exiftool` on macOS)
2. **Backup**: Always backup your photos before using --move
3. **Duplicates**: The script won't overwrite existing files
4. **Performance**: Uses parallel processing for faster analysis
5. **Cache**: EXIF data is cached to speed up re-analysis

## Troubleshooting

- **"Target already exists"**: File already exists in destination
- **Slow performance**: Disable cache or reduce max_workers in config
- **Memory issues**: Script automatically handles large collections with streaming