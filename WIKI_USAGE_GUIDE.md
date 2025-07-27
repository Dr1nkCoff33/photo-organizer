# Photo Organizer Usage Guide Wiki

> **Quick Start**: `python -m src.quick_analyze /path/to/photos`

This wiki provides comprehensive documentation for the enhanced photo organizer with Claude AI integration, improved accuracy, and simplified output.

## Table of Contents

1. [Quick Start](#-quick-start)
2. [Installation](#-installation)
3. [Basic Usage](#-basic-usage)
4. [Advanced Features](#-advanced-features)
5. [Claude AI Integration](#-claude-ai-integration)
6. [Configuration](#-configuration)
7. [Output Formats](#-output-formats)
8. [Troubleshooting](#-troubleshooting)
9. [Performance Tips](#-performance-tips)
10. [API Reference](#-api-reference)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- ExifTool installed on your system
- Optional: Claude API key for AI-powered analysis

### Installation
```bash
# Clone the repository
git clone https://github.com/Dr1nkCoff33/photo-organizer.git
cd photo-organizer

# Install dependencies
pip install -r requirements.txt

# Install ExifTool (macOS)
brew install exiftool

# Install ExifTool (Ubuntu/Debian)
sudo apt-get install exiftool
```

### First Run
```bash
# Quick analysis with minimal output
python -m src.quick_analyze /path/to/photos

# With Claude AI (requires API key)
export CLAUDE_API_KEY="your-api-key-here"
python -m src.quick_analyze /path/to/photos --claude
```

## 📊 Basic Usage

### Command Line Interface

#### Quick Analysis Tool
```bash
# Basic analysis
python -m src.quick_analyze /path/to/photos

# With custom output directory
python -m src.quick_analyze /path/to/photos --output-dir /path/to/results

# With Claude AI
python -m src.quick_analyze /path/to/photos --claude

# Organize photos after analysis
python -m src.quick_analyze /path/to/photos --organize

# Use custom configuration
python -m src.quick_analyze /path/to/photos --config config/enhanced_photo_analyzer_config.yaml
```

#### Enhanced Analyzer
```bash
# Full analysis with detailed output
python src/analyze_photos_exif.py /path/to/photos /path/to/output

# With custom configuration
python src/analyze_photos_exif.py /path/to/photos /path/to/output --config config/enhanced_photo_analyzer_config.yaml

# Organize photos
python src/analyze_photos_exif.py /path/to/photos /path/to/output --organize --move
```

### Python API
```python
from src.analyze_photos_exif import main, PhotoAnalyzerConfig

# Load custom configuration
config = PhotoAnalyzerConfig('config/enhanced_photo_analyzer_config.yaml')

# Run analysis
result = main('/path/to/photos', '/path/to/output', 'config/enhanced_photo_analyzer_config.yaml')

# Access results
print(f"Total photos: {result['summary']['total_files']}")
print(f"Categories: {result['summary']['analyzed_categories']}")
```

## 🎯 Advanced Features

### Category Detection

The enhanced analyzer uses sophisticated algorithms to categorize photos:

#### Portrait Photography
- **Focal Length**: 50-135mm
- **Aperture**: f/2.8 or wider
- **Focus Mode**: AF-S, Single Point
- **Scene Mode**: Portrait
- **Confidence Threshold**: 3.0

#### Landscape Photography
- **Focal Length**: 0-35mm
- **Aperture**: f/8 or narrower
- **Focus Mode**: AF-S, Manual
- **Scene Mode**: Landscape
- **Confidence Threshold**: 3.0

#### Street Photography
- **Focal Length**: 28-50mm
- **Aperture**: f/3.5-f/8
- **Focus Mode**: AF-C, Continuous AF
- **ISO**: 400+ (for low light)
- **Confidence Threshold**: 3.0

#### Event Photography
- **Burst Sequences**: 5+ photos within 1 second
- **Focus Mode**: AF-C
- **Auto-detected from timing**
- **Confidence Threshold**: 2.0

#### Wildlife/Sports
- **Focal Length**: 200mm+
- **Focus Mode**: AF-C, Continuous AF
- **Shutter Speed**: 1/500s or faster
- **Confidence Threshold**: 3.0

#### Macro Photography
- **Lens**: Contains "macro" in name
- **Subject Distance**: <50cm
- **Aperture**: f/8+ for depth of field
- **Confidence Threshold**: 4.0

#### Night Photography
- **ISO**: 1600+
- **Scene Mode**: Night
- **Aperture**: f/2.8+ for low light
- **Confidence Threshold**: 3.0

#### Architecture
- **Focal Length**: 0-24mm
- **Aperture**: f/5.6-f/11
- **Focus Mode**: AF-S, Manual
- **Confidence Threshold**: 3.0

### Burst Detection
The analyzer automatically detects burst sequences:
- Groups photos taken within 1 second of each other
- Identifies sequences of 5+ photos as events
- Provides burst statistics in output

## 🤖 Claude AI Integration

### Setup
1. Get a Claude API key from [Anthropic Console](https://console.anthropic.com/)
2. Set environment variable:
   ```bash
   export CLAUDE_API_KEY="your-api-key-here"
   ```

### How It Works
- Analyzes a sample of photos (default: 20)
- Prioritizes uncategorized photos
- Provides content-based validation
- Can override EXIF-based categories with high confidence (8+)

### Benefits
- **Better Accuracy**: Content-aware categorization
- **Reduced False Positives**: Validates EXIF-based decisions
- **Handles Edge Cases**: Identifies photos that EXIF alone might miss

### Usage
```bash
# Enable Claude AI analysis
python -m src.quick_analyze /path/to/photos --claude

# With custom sample size
# Edit config/enhanced_photo_analyzer_config.yaml:
claude_analysis:
  enabled: true
  sample_size: 30  # Analyze 30 photos instead of 20
  confidence_threshold: 8
```

## ⚙️ Configuration

### Basic Configuration
```yaml
# config/photo_analyzer_config.yaml
max_workers: 8
batch_size: 50
cache_enabled: true

categories:
  Portrait:
    focal_range: [50, 135]
    f_number_max: 2.8
    weight: 1.0
```

### Enhanced Configuration
```yaml
# config/enhanced_photo_analyzer_config.yaml
claude_analysis:
  enabled: true
  sample_size: 20
  confidence_threshold: 8

categories:
  Portrait:
    focal_range: [50, 135]
    f_number_max: 2.8
    weight: 1.0
    confidence_threshold: 3.0

output:
  create_simplified_report: true
  create_json_summary: true
  include_claude_analysis: true
  max_mismatch_samples: 50

advanced:
  confidence_threshold: 3.0
  burst_time_threshold: 1.0
  enable_negative_scoring: true
  prioritize_claude_for_uncategorized: true
```

### Custom Categories
```yaml
categories:
  Astrophotography:
    iso_min: 3200
    weight: 1.5
    confidence_threshold: 4.0
    
  Documentary:
    focal_range: [35, 85]
    weight: 1.2
    confidence_threshold: 3.0
```

## 📄 Output Formats

### 1. Analysis Summary (analysis_summary.txt)
```
📸 PHOTO ANALYSIS SUMMARY
==================================================
📅 Date: 2024-01-15 14:30:25
📁 Total Photos: 225
📅 Date Range: 2024:09:08 18:02:09 to 2024:09:08 18:36:17

📊 CATEGORY BREAKDOWN
------------------------------
  Event          170 photos ( 75.6%)
  Street          40 photos ( 17.8%)
  Landscape       14 photos (  6.2%)
  Portrait         1 photos (  0.4%)

🎯 BURST DETECTION
------------------------------
  Burst Sequences: 31
  Burst Photos: 170 (75.6%)

🔄 CATEGORY CHANGES
------------------------------
  Lifestyle       → 50 photos reclassified
  Portrait        → 70 photos reclassified
  Total Changes: 120 (53.3%)
```

### 2. JSON Summary (analysis_summary.json)
```json
{
  "metadata": {
    "timestamp": "2024-01-15T14:30:25.123456",
    "total_photos": 225,
    "date_range": {
      "start": "2024:09:08 18:02:09",
      "end": "2024:09:08 18:36:17"
    }
  },
  "categories": {
    "Event": 170,
    "Street": 40,
    "Landscape": 14,
    "Portrait": 1
  },
  "burst_info": {
    "sequences": 31,
    "photos": 170
  },
  "changes": {
    "total_changes": 120,
    "change_percentage": 53.3
  }
}
```

### 3. Detailed Analysis (exif_analysis_results.json)
Contains comprehensive data including:
- Full EXIF data for each photo
- Category comparison details
- Sample mismatches
- Claude AI analysis results (if enabled)

## 🐛 Troubleshooting

### Common Issues

#### 1. "exiftool not found"
```bash
# macOS
brew install exiftool

# Ubuntu/Debian
sudo apt-get install exiftool

# Windows
# Download from https://exiftool.org/
```

#### 2. Claude API errors
- Verify API key is set correctly: `echo $CLAUDE_API_KEY`
- Check internet connection
- Ensure sufficient API credits
- Verify API key format and permissions

#### 3. Memory errors with large collections
```yaml
# Reduce in config file
max_workers: 4
batch_size: 25
```

#### 4. Slow performance
- Enable caching: `cache_enabled: true`
- Increase workers: `max_workers: 12` (up to CPU count + 4)
- Use SSD storage if possible
- Reduce batch size for HDD storage

### Performance Tuning

#### For Large Collections (>10,000 photos)
```yaml
# Enable streaming processing
batch_size: 100
max_workers: 12
cache_enabled: true
```

#### For Memory-Constrained Systems
```yaml
batch_size: 20
max_workers: 2
cache_enabled: true
```

#### For Best Accuracy
```yaml
claude_analysis:
  enabled: true
  sample_size: 30
  confidence_threshold: 8

advanced:
  enable_negative_scoring: true
  prioritize_claude_for_uncategorized: true
```

## 📈 Performance Benchmarks

| Collection Size | EXIF Only | With Claude AI | Speedup vs Original |
|----------------|-----------|----------------|-------------------|
| 1,000 photos   | 2-3 min   | 5-8 min        | 15-20x faster     |
| 5,000 photos   | 8-12 min  | 20-30 min      | 20-30x faster     |
| 10,000 photos  | 15-25 min | 40-60 min      | 25-35x faster     |

*Performance on MacBook Pro M1 with 16GB RAM*

## 🔧 Advanced Usage

### Batch Processing
```bash
# Process multiple directories
for dir in /path/to/photo_collections/*; do
    python -m src.quick_analyze "$dir" \
        --output-dir "/path/to/results/$(basename "$dir")" \
        --config config/enhanced_photo_analyzer_config.yaml
done
```

### Integration with Other Tools
```python
# Use in your own scripts
from src.analyze_photos_exif import main
from src.claude_analyzer import ClaudePhotoAnalyzer

# Run analysis
result = main('/path/to/photos', '/path/to/output')

# Access Claude analyzer
claude = ClaudePhotoAnalyzer()
if claude.enabled:
    # Analyze specific photo
    analysis = claude.analyze_photo_content('/path/to/photo.jpg', exif_data)
```

### Custom Category Detection
```python
# Extend the analyzer with custom categories
def custom_category_detector(exif_data, config):
    # Your custom logic here
    if custom_condition:
        return "CustomCategory"
    return None
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review configuration examples
3. Test with a small sample first
4. Check detailed logs in output directory

### Reporting Issues
- Include your configuration file
- Provide sample EXIF data
- Include error messages and stack traces
- Specify system details (OS, Python version, etc.)

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

**Last Updated**: January 2024  
**Version**: Enhanced Photo Analyzer v2.0  
**Author**: Photo Organizer Team 