# Photo Organizer Usage Guide

## 🚀 Quick Start

### Basic Analysis
```bash
# Quick analysis with minimal output
python -m src.quick_analyze /path/to/photos

# With custom output directory
python -m src.quick_analyze /path/to/photos --output-dir /path/to/results
```

### Enhanced Analysis with Claude AI
```bash
# Set your Claude API key
export CLAUDE_API_KEY="your-api-key-here"

# Run analysis with Claude AI content validation
python -m src.quick_analyze /path/to/photos --claude

# Use enhanced configuration
python -m src.quick_analyze /path/to/photos --config config/enhanced_photo_analyzer_config.yaml --claude
```

### Organize Photos
```bash
# Analyze and organize photos into category folders
python -m src.quick_analyze /path/to/photos --organize

# Use custom configuration for organization
python -m src.quick_analyze /path/to/photos --config config/enhanced_photo_analyzer_config.yaml --organize
```

## 📊 Output Files

The analyzer generates several output files:

### 1. `analysis_summary.txt` - Human-readable summary
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

### 2. `analysis_summary.json` - Simplified JSON data
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

### 3. `exif_analysis_results.json` - Detailed analysis (for advanced users)
Contains comprehensive data including:
- Full EXIF data for each photo
- Category comparison details
- Sample mismatches
- Claude AI analysis results (if enabled)

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

### Enhanced Configuration with Claude AI
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
```

## 🎯 Category Detection

### Portrait Photography
- **Focal Length**: 50-135mm
- **Aperture**: f/2.8 or wider
- **Focus Mode**: AF-S, Single Point
- **Scene Mode**: Portrait

### Landscape Photography
- **Focal Length**: 0-35mm
- **Aperture**: f/8 or narrower
- **Focus Mode**: AF-S, Manual
- **Scene Mode**: Landscape

### Street Photography
- **Focal Length**: 28-50mm
- **Aperture**: f/3.5-f/8
- **Focus Mode**: AF-C, Continuous AF
- **ISO**: 400+ (for low light)

### Event Photography
- **Burst Sequences**: 5+ photos within 1 second
- **Focus Mode**: AF-C
- **Auto-detected from timing**

### Wildlife/Sports
- **Focal Length**: 200mm+
- **Focus Mode**: AF-C, Continuous AF
- **Shutter Speed**: 1/500s or faster

### Macro Photography
- **Lens**: Contains "macro" in name
- **Subject Distance**: <50cm
- **Aperture**: f/8+ for depth of field

### Night Photography
- **ISO**: 1600+
- **Scene Mode**: Night
- **Aperture**: f/2.8+ for low light

### Architecture
- **Focal Length**: 0-24mm
- **Aperture**: f/5.6-f/11
- **Focus Mode**: AF-S, Manual

## 🤖 Claude AI Integration

### Setup
1. Get a Claude API key from [Anthropic](https://console.anthropic.com/)
2. Set environment variable:
   ```bash
   export CLAUDE_API_KEY="your-api-key-here"
   ```

### How it Works
- Analyzes a sample of photos (default: 20)
- Prioritizes uncategorized photos
- Provides content-based validation
- Can override EXIF-based categories with high confidence

### Benefits
- **Better Accuracy**: Content-aware categorization
- **Reduced False Positives**: Validates EXIF-based decisions
- **Handles Edge Cases**: Identifies photos that EXIF alone might miss

## 🔧 Advanced Usage

### Custom Category Definitions
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

### Performance Tuning
```yaml
# For SSD storage
batch_size: 100
max_workers: 12

# For HDD storage
batch_size: 25
max_workers: 4

# For memory-constrained systems
batch_size: 20
max_workers: 2
```

### Batch Processing
```bash
# Process multiple directories
for dir in /path/to/photo_collections/*; do
    python -m src.quick_analyze "$dir" --output-dir "/path/to/results/$(basename "$dir")"
done
```

## 🐛 Troubleshooting

### Common Issues

1. **"exiftool not found"**
   ```bash
   # macOS
   brew install exiftool
   
   # Ubuntu/Debian
   sudo apt-get install exiftool
   ```

2. **Claude API errors**
   - Verify API key is set correctly
   - Check internet connection
   - Ensure sufficient API credits

3. **Memory errors with large collections**
   - Reduce `batch_size` in configuration
   - Reduce `max_workers`
   - Enable streaming processing for >10,000 files

4. **Slow performance**
   - Enable caching
   - Increase `max_workers` (up to CPU count + 4)
   - Use SSD storage if possible

### Performance Tips

1. **For Large Collections (>10,000 photos)**
   - Use streaming processing
   - Enable caching
   - Process in batches

2. **For Frequent Analysis**
   - Keep cache enabled
   - Use progress tracking
   - Consider incremental analysis

3. **For Best Accuracy**
   - Enable Claude AI analysis
   - Use enhanced configuration
   - Review and adjust category thresholds

## 📈 Expected Performance

| Collection Size | EXIF Only | With Claude AI | Speedup vs Original |
|----------------|-----------|----------------|-------------------|
| 1,000 photos   | 2-3 min   | 5-8 min        | 15-20x faster     |
| 5,000 photos   | 8-12 min  | 20-30 min      | 20-30x faster     |
| 10,000 photos  | 15-25 min | 40-60 min      | 25-35x faster     |

*Performance on MacBook Pro M1 with 16GB RAM*

## 🔄 Migration from Old Version

If you're upgrading from the previous version:

1. **Backup your data**
   ```bash
   cp -r output/ output_backup/
   ```

2. **Update configuration**
   ```bash
   cp config/enhanced_photo_analyzer_config.yaml config/my_config.yaml
   # Edit my_config.yaml as needed
   ```

3. **Run analysis with new system**
   ```bash
   python -m src.quick_analyze /path/to/photos --config config/my_config.yaml
   ```

4. **Compare results**
   - Check `analysis_summary.txt` for overview
   - Review category changes in the report
   - Validate with Claude AI if enabled

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the configuration examples
3. Test with a small sample first
4. Check the detailed logs in the output directory 