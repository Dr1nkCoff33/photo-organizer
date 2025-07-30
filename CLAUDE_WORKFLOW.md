# Claude Code Photo Organization Workflow

## Quick Start - Organizing Photos from SD Card

### 1. Insert SD Card
Your SD card will typically mount at:
- `/Volumes/[CARD_NAME]/DCIM/` (macOS)

### 2. Use the Unified Photo Analyze Command

Choose your analysis mode based on needs:

```bash
# Enhanced analysis (default) - Best for most cases
/photo-analyze /Volumes/SDCard/DCIM

# Quick analysis - For large collections or quick overview
/photo-analyze /Volumes/SDCard/DCIM --mode=quick

# Claude AI analysis - For maximum accuracy
/photo-analyze /Volumes/SDCard/DCIM --mode=claude --organize

# Custom output location
/photo-analyze /Volumes/SDCard/DCIM --output=~/Pictures/Organized --organize
```

### 3. What Each Mode Does

#### Quick Mode
- **Speed**: 1-2 min per 1000 photos
- **Analysis**: Basic EXIF extraction
- **Best for**: Initial surveys, large collections

#### Enhanced Mode (Default)
- **Speed**: 3-5 min per 1000 photos  
- **Analysis**: Full EXIF + burst detection
- **Best for**: Most photo organization tasks

#### Claude Mode
- **Speed**: 10-15 min per 1000 photos
- **Analysis**: Enhanced + AI content validation
- **Best for**: Maximum accuracy, important collections

### 4. Output Structure
```
Output/
├── Portrait/
│   └── 2024-01/
├── Landscape/
│   └── 2024-01/
├── Street/
│   └── 2024-01/
├── Event/
│   └── 2024-01/
├── analysis_summary.txt
├── analysis_summary.json
└── exif_analysis_results.json
```

## Advanced Usage

### Mode Selection Guidelines

**Use Quick Mode when:**
- Processing 10,000+ photos
- Need a fast overview
- Limited time available
- Initial collection survey

**Use Enhanced Mode when:**
- Standard photo organization
- Balanced speed/accuracy needed
- Processing 1,000-5,000 photos
- Default choice for most tasks

**Use Claude Mode when:**
- Maximum accuracy required
- Difficult to categorize photos
- Important collections
- Content validation needed

### Custom Parameters
```bash
# Claude mode with custom sample size
/photo-analyze /path/to/photos --mode=claude --sample=50

# Enhanced mode with move instead of copy
/photo-analyze /path/to/photos --mode=enhanced --organize --move

# Quick mode with verbose output
/photo-analyze /path/to/photos --mode=quick --verbose
```

## Tips

1. **First Run**: Try analysis-only mode first to preview categorization
2. **Backup**: SD cards are safe - Claude copies files, doesn't move them
3. **Performance**: Claude can handle thousands of photos efficiently
4. **Verification**: Ask Claude to show you sample categorizations before full processing

## Setup and Requirements

### Built-in Tools
- ExifTool for EXIF analysis (pre-installed)
- Photo processing capabilities
- File organization system

### Optional Setup
- Claude API key for AI mode: `export CLAUDE_API_KEY="your-key"`
- Run `/project-setup` for environment validation

### No Installation Required
- All core functionality works out of the box
- Claude Code handles all dependencies
- Just run commands and start organizing
