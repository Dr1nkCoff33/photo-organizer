# Claude Code Photo Organization Workflow

## Quick Start - Organizing Photos from SD Card

### 1. Insert SD Card
Your SD card will typically mount at:
- `/Volumes/[CARD_NAME]/DCIM/` (macOS)

### 2. Use Claude Code to Analyze and Organize

Simply run one of these commands:

```bash
# Basic organization by date and EXIF analysis
claude "Organize my RAW photos from /Volumes/SDCard/DCIM"

# With specific categorization
claude "Use the photo-organizer-raw agent to analyze photos in /Volumes/SDCard/DCIM and categorize them by:
- Portrait (50-135mm focal length)
- Landscape (wide angle)
- Street photography
- Event/burst sequences
Then organize them into folders by category and date"

# Custom output location
claude "Organize photos from /Volumes/SDCard/DCIM to ~/Pictures/Organized with EXIF categorization"
```

### 3. What Claude Code Will Do

The built-in `photo-organizer-raw` agent will:
1. **Read EXIF data** from all RAW files (ARW, CR2, NEF, etc.)
2. **Analyze metadata**:
   - Focal length for composition type
   - Aperture for depth of field
   - ISO and shutter speed
   - Burst sequences for events
3. **Categorize photos** based on shooting patterns
4. **Organize files** into a structure like:
   ```
   Output/
   ├── Portrait/
   │   └── 2024-01/
   ├── Landscape/
   │   └── 2024-01/
   ├── Street/
   │   └── 2024-01/
   └── Events/
       └── 2024-01/
   ```

## Advanced Usage

### Custom Categories
```bash
claude "Analyze my photos and create custom categories based on:
- Wildlife (telephoto >200mm)
- Macro (close focus distance)
- Architecture (ultra-wide <24mm)
- Night photography (high ISO)"
```

### Analysis Only (No Moving Files)
```bash
claude "Analyze EXIF data from /Volumes/SDCard/DCIM and create a report without moving files"
```

### Facial Detection
```bash
claude "Organize photos and group those with detected faces into a separate folder"
```

## Tips

1. **First Run**: Try analysis-only mode first to preview categorization
2. **Backup**: SD cards are safe - Claude copies files, doesn't move them
3. **Performance**: Claude can handle thousands of photos efficiently
4. **Verification**: Ask Claude to show you sample categorizations before full processing

## No Setup Required!

- No Python installation needed
- No config files to edit
- ExifTool is already available to Claude Code
- Just run the command and Claude handles everything
