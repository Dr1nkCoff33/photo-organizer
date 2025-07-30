# Photo Organizer

A streamlined Claude Code workflow for organizing photos using EXIF analysis and optional Claude AI integration. Features a unified command system with three analysis modes to match your needs.

## What It Does

This tool reads the metadata from your RAW photos (like focal length, aperture, and shooting mode) to figure out what type of photo it is. Then it organizes them into folders by category and date.

**Key Features:**
- Analyzes EXIF data to categorize photos correctly
- Detects burst sequences and groups them as events
- Organizes photos by category and date
- Optionally uses Claude AI to verify categories
- Processes thousands of photos in minutes

## Quick Start

### Using the Unified Command

```bash
# Enhanced analysis (default mode)
/photo-analyze /path/to/photos

# Quick analysis for large collections
/photo-analyze /path/to/photos --mode=quick

# Full Claude AI analysis
/photo-analyze /path/to/photos --mode=claude --organize

# Custom output location
/photo-analyze /path/to/photos --output=/external/drive/results
```

### Analysis Modes

- **Quick**: Basic EXIF analysis (fastest)
- **Enhanced**: Full EXIF + burst detection (default)
- **Claude**: Enhanced + AI content validation

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

The `photo-organizer-core` agent:
1. Reads EXIF metadata from all photo files
2. Analyzes shooting patterns based on selected mode
3. Detects burst sequences and time clusters
4. Optionally validates with Claude AI
5. Organizes photos into categorized folders by date

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
# Default enhanced analysis
/photo-analyze /Volumes/SDCard/DCIM

# Quick analysis with organization
/photo-analyze /Volumes/SDCard/DCIM --mode=quick --organize

# Claude AI analysis with custom sample size
/photo-analyze /path/to/photos --mode=claude --sample=30

# Specify output and organize
/photo-analyze /path/to/photos --output=/external/drive --organize --move
```

## Performance

| Mode | 1,000 photos | 5,000 photos | 10,000 photos |
|------|--------------|--------------|---------------|
| Quick | 1-2 min | 5-8 min | 10-15 min |
| Enhanced | 3-5 min | 15-20 min | 30-40 min |
| Claude | 10-15 min | 30-45 min | 60-90 min |

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
