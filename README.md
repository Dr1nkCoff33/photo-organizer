# Photo Organizer

A fast Python tool that organizes your RAW photos by analyzing their EXIF data. It automatically sorts photos into categories like Portrait, Landscape, Street, and Event based on how you actually shot them.

## What It Does

This tool reads the metadata from your RAW photos (like focal length, aperture, and shooting mode) to figure out what type of photo it is. Then it organizes them into folders by category and date.

**Key Features:**
- Analyzes EXIF data to categorize photos correctly
- Detects burst sequences and groups them as events
- Organizes photos by category and date
- Optionally uses Claude AI to verify categories
- Processes thousands of photos in minutes

## Quick Start

### Install Requirements

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install ExifTool:
```bash
# Mac
brew install exiftool

# Linux
sudo apt-get install exiftool
```

### Basic Usage

The tool will always ask you where to save the results:

```bash
# Just analyze photos
python organize_photos.py /path/to/your/photos

# Analyze and organize into folders
python organize_photos.py /path/to/your/photos --organize

# Use the quick analyzer
python -m src.quick_analyze /path/to/your/photos
```

### Using Claude AI

For better accuracy, you can use Claude AI to verify photo categories:

1. Get an API key from [Anthropic](https://console.anthropic.com/)
2. Set the environment variable:
```bash
export CLAUDE_API_KEY="your-api-key-here"
```
3. Run with Claude:
```bash
python -m src.quick_analyze /path/to/your/photos --claude
```

## How Categories Work

The tool looks at your camera settings to determine photo types:

**Portrait** - Medium telephoto (50-135mm), wide aperture (f/2.8 or wider)
**Landscape** - Wide angle (0-35mm), narrow aperture (f/8 or smaller)  
**Street** - Standard focal length (28-50mm), medium aperture
**Event** - Burst sequences (5+ photos within 1 second)
**Wildlife/Sports** - Long telephoto (200mm+), fast shutter speed
**Architecture** - Ultra-wide (0-24mm), medium aperture
**Macro** - Macro lens or very close focus distance
**Night** - High ISO (1600+) or night scene mode

## Configuration

You can customize settings in `config/enhanced_photo_analyzer_config.yaml`:

```yaml
# Performance settings
max_workers: 8        # Parallel processing threads
batch_size: 50        # Files processed per batch
cache_enabled: true   # Cache EXIF data for speed

# Category settings
categories:
  Portrait:
    focal_range: [50, 135]
    f_number_max: 2.8
    confidence_threshold: 3.0
```

## Output Structure

When you organize photos, they'll be sorted like this:

```
your_output_folder/
├── Portrait/
│   └── 2024-09/
│       └── 20240908-IMG_001.ARW
├── Landscape/
│   └── 2024-09/
│       └── 20240908-IMG_002.ARW
├── Event/
│   └── 2024-09/
│       └── [burst sequences]
├── analysis_summary.txt      # Human-readable summary
├── analysis_summary.json     # Simple JSON data
└── exif_analysis_results.json # Detailed analysis data
```

## Command Options

**organize_photos.py:**
- `source_dir` - Your photo folder (required)
- `--organize` - Sort photos into category folders
- `--move` - Move files instead of copying (use carefully!)
- `--config` - Use a custom config file

**quick_analyze.py:**
- `source_dir` - Your photo folder (required)
- `--output-dir` - Where to save results (will prompt if not provided)
- `--claude` - Use Claude AI for better accuracy
- `--organize` - Sort photos after analysis
- `--config` - Use a custom config file

## Performance

On a modern computer:
- 1,000 photos: 2-3 minutes
- 5,000 photos: 8-12 minutes  
- 10,000 photos: 15-25 minutes

With Claude AI enabled, add about 2-3x more time.

## Tips

1. **First Time**: Try analyzing without organizing to see the results first
2. **Large Collections**: The tool handles 10,000+ photos efficiently
3. **Storage**: Keep your photos on a fast SSD for best performance
4. **Backups**: Always backup before using `--move` option

## Troubleshooting

**"exiftool not found"** - Install it with `brew install exiftool` (Mac) or `apt-get install exiftool` (Linux)

**Claude API errors** - Check your API key is set correctly with `echo $CLAUDE_API_KEY`

**Slow performance** - Enable caching in the config file and use an SSD

**Memory errors** - Reduce `batch_size` in the config file

## License

MIT License