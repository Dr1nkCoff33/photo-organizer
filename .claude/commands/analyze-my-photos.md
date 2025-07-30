---
allowed-tools: Bash, Read, Edit, Grep, Glob, WebFetch
description: Main command for photo analysis with EXIF and optional Claude AI integration
argument-hint: [directory] [--claude] [--organize] [--sample=N] [--verbose]
---

# Analyze My Photos Command

## Command: `/analyze-my-photos`

### Description
**Your main command for photo analysis** - Simple, powerful, and optimized for your personal workflow. This command handles everything from basic analysis to full Claude AI integration with automatic environment setup and intelligent defaults.

### Usage
```
/analyze-my-photos [directory] [options]
```

### Parameters
- `directory`: Directory containing photos (will prompt if not provided)
- `output`: Output directory for results (will prompt if not provided)
- `--claude`: Enable Claude AI content analysis (recommended)
- `--enhanced`: Use enhanced EXIF analysis (default)
- `--basic`: Use basic analysis (faster, no EXIF)
- `--organize`: Organize photos by date and category
- `--move`: Move files instead of copying
- `--verbose`: Show detailed progress
- `--config=path`: Use custom configuration file
- `--sample=N`: Number of photos for Claude AI analysis (will prompt if not provided, default: 20)
- `--confidence=N`: Minimum confidence for category overrides (default: 8)

### Examples
```
# Standard analysis with Claude AI (will prompt for directories and sample size)
/analyze-my-photos --claude

# Specify source directory, prompt for output
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --claude

# Full analysis with all parameters
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 /external/drive/photo-output --claude --organize

# Quick analysis without Claude AI
/analyze-my-photos --basic

# Enhanced analysis with custom settings
/analyze-my-photos --claude --sample=30 --confidence=7 --verbose

# Full analysis with file moving and custom config
/analyze-my-photos --claude --organize --move --config=config/enhanced_photo_analyzer_config.yaml --verbose
```

### Workflow
1. **Directory Prompts** - Ask for input/output directories if not provided
2. **Sample Size Prompt** - Ask for Claude AI sample size if --claude is used
3. **Environment Setup** - Source .env file and verify Claude API key
4. **Path Validation** - Verify the directories exist
5. **ExifTool Check** - Ensure exiftool is available for enhanced analysis
6. **Claude AI Setup** - Verify Claude API key and connectivity
7. **Script Execution** - Run the appropriate Python analysis script
8. **Progress Monitoring** - Track analysis progress and handle errors
9. **Results Summary** - Display analysis results and statistics
10. **Organization** - Organize files if requested

### Python Script Execution
The command automatically runs the appropriate Python scripts:

**Recommended - Quick Analysis with Claude AI:**
```bash
# Source environment and run quick analysis (prompts for output dir)
source .env
python -m src.quick_analyze [directory] --claude --organize
```

**Enhanced Analysis with Claude AI:**
```bash
# Source environment and run enhanced analysis (prompts for output dir)
source .env
python -m src.quick_analyze [directory] --output-dir [output_directory] --claude --config config/enhanced_photo_analyzer_config.yaml --organize
```

**Legacy Enhanced Analysis:**
```bash
python organize_photos.py [directory] --output-dir [output_directory] --organize --move
```

**Basic Analysis:**
```bash
python organize_photos.py [directory] --output-dir [output_directory]
```

### Output Structure
The analysis results will be saved to your specified output directory:
```
[your_output_directory]/
├── analysis_summary.txt          # Human-readable summary
├── analysis_summary.json         # Structured data
├── exif_analysis_results.json    # Detailed EXIF analysis
└── organized/                    # Organized photos (if requested)
    ├── Portrait/
    │   └── 2024-09/
    │       └── photo.ARW
    ├── Landscape/
    │   └── 2024-09/
    │       └── photo.ARW
    ├── Event/
    │   └── 2024-09/
    │       └── photo.ARW
    └── Street/
        └── 2024-09/
            └── photo.ARW
```

### Expected Results
- **File Count**: Total number of photos processed
- **Categories**: Breakdown by photo type (Portrait, Landscape, etc.)
- **Claude AI Analysis**: Content-aware categorization results
- **Burst Sequences**: Detection of photo sequences
- **Date Range**: Earliest and latest photo dates
- **File Sizes**: Total size and average file size
- **Processing Time**: How long the analysis took
- **Organization**: Where files were moved/organized
- **Confidence Scores**: Claude AI confidence levels for categorizations

### Claude AI Integration
When `--claude` is used:
- **Sample Analysis**: Analyzes 20 sample photos by default (configurable with --sample)
- **Content Validation**: Validates EXIF-based categorizations
- **Edge Case Handling**: Identifies photos that EXIF alone might miss
- **Confidence Scoring**: Provides confidence levels for each categorization
- **Category Overrides**: Can override EXIF categories with high confidence (configurable with --confidence)

### Error Handling
- **Missing Directory**: Clear error message with suggestions
- **No Photos Found**: Guidance on supported file types
- **ExifTool Issues**: Automatic detection and installation help
- **Claude API Issues**: Verification of API key and connectivity
- **Permission Errors**: Clear instructions for fixing permissions
- **Memory Issues**: Suggestions for handling large collections

### Performance Tips
- **Large Collections**: Use `--basic` for collections over 10,000 files
- **Network Drives**: Consider copying to local drive first
- **Memory**: Close other applications for very large collections
- **Caching**: Subsequent runs will be faster due to caching
- **Claude AI**: Sample analysis keeps processing time reasonable
- **Custom Sampling**: Use `--sample=10` for faster analysis, `--sample=50` for higher accuracy

### Interactive Prompts
When directories or sample size are not provided, you'll see:

```
📂 Where are your photos located?
   (Enter full path to photo directory)
   Photo directory: /Users/carlosmartinez/Documents/2024-09-08

📂 Where should I save the analysis results?
   (Enter full path to output directory)
   Output directory: /external/drive/photo-analysis/2024-09-08

🤖 How many photos should Claude AI analyze?
   (Enter number between 5-100, or press Enter for default: 20)
   Sample size: 30
```

### Sample Output
```
📸 Quick Photo Analysis
📁 Source: /Users/carlosmartinez/Documents/2024-09-08
📂 Output: /external/drive/photo-analysis/2024-09-08
🤖 Claude AI: Enabled (30 photo sample)
📦 Organize: No
--------------------------------------------------

✅ Analysis Complete!
📊 Total Photos: 225

📈 Top Categories:
  Event          170 photos ( 75.6%)
  Street          40 photos ( 17.8%)
  Landscape       14 photos (  6.2%)
  Portrait         1 photos (  0.4%)

🎯 Burst Sequences: 31

🤖 Claude AI Analysis:
  - 30 photos analyzed with Claude AI
  - 3 category overrides applied
  - Average confidence: 8.2/10
  - Content validation: 95% accuracy

📄 Results saved to: /external/drive/photo-analysis/2024-09-08
```

### Why This Command?
- **🎯 One Command Does Everything**: From basic analysis to full Claude AI integration
- **🚀 Optimized for Your Workflow**: Designed specifically for your directory structure
- **🤖 Smart Defaults**: Intelligent parameter selection based on your needs
- **📊 Comprehensive Results**: Everything you need to know about your photos
- **🔧 Easy to Use**: Simple parameters, clear output, helpful error messages
