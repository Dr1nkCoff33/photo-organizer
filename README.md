# Photo Organizer

A Claude Code workflow for organizing RAW photos by analyzing their EXIF data. Uses Claude's built-in photo-organizer-raw agent to automatically sort photos into categories like Portrait, Landscape, Street, and Event based on how you actually shot them.

## What It Does

This tool reads the metadata from your RAW photos (like focal length, aperture, and shooting mode) to figure out what type of photo it is. Then it organizes them into folders by category and date.

**Key Features:**
- Analyzes EXIF data to categorize photos correctly
- Detects burst sequences and groups them as events
- Organizes photos by category and date
- Optionally uses Claude AI to verify categories
- Processes thousands of photos in minutes

## Quick Start

### No Installation Required!

Claude Code has everything built-in. Just run:

```bash
# Basic organization
claude "Organize my RAW photos from /Volumes/SDCard/DCIM"

# With specific output location
claude "Organize photos from /Volumes/SDCard/DCIM to ~/Pictures/Organized"

# Analysis only (no file moving)
claude "Analyze EXIF data from /path/to/photos and create a report"
```

### Advanced Categorization

Claude automatically analyzes EXIF data and can create custom categories:

```bash
# Custom categories based on your shooting style
claude "Analyze my photos and categorize by focal length, aperture, and shooting patterns"

# With facial detection
claude "Organize photos and group portraits with detected faces"
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

## How It Works

Claude Code's `photo-organizer-raw` agent:
1. Reads EXIF metadata from all RAW files
2. Analyzes shooting patterns (focal length, aperture, ISO)
3. Detects burst sequences for events
4. Organizes photos into categorized folders by date

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

## Example Commands

```bash
# From SD card to organized folders
claude "Organize RAW photos from /Volumes/SDCard/DCIM"

# Custom categories
claude "Create categories for wildlife, macro, and architecture photos"

# Analysis report only
claude "Generate EXIF analysis report for my photo collection"

# Specific date range
claude "Organize photos from January 2024 only"
```

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

## See Also

- [CLAUDE_WORKFLOW.md](CLAUDE_WORKFLOW.md) - Detailed workflow guide
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT License
