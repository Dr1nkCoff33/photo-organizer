# Analyze My Photos Command

## Command: `/analyze-my-photos`

### Description
**Your main command for photo analysis** - Simple, powerful, and optimized for your personal workflow. This command handles everything from basic analysis to full Claude AI integration with automatic environment setup and intelligent defaults.

### Usage
```
/analyze-my-photos [directory] [options]
```

### Parameters
- `directory`: Directory containing photos (e.g., /Users/carlosmartinez/Documents/2024-09-08)
- `--claude`: Enable Claude AI content analysis (recommended)
- `--enhanced`: Use enhanced EXIF analysis (default)
- `--basic`: Use basic analysis (faster, no EXIF)
- `--organize`: Organize photos by date and category
- `--move`: Move files instead of copying
- `--clean`: Clean output before analysis
- `--verbose`: Show detailed progress
- `--config=path`: Use custom configuration file
- `--sample=N`: Number of photos for Claude AI analysis (default: 20)
- `--confidence=N`: Minimum confidence for category overrides (default: 8)

### Examples
```
# Standard analysis with Claude AI (recommended)
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --claude

# Full analysis with Claude AI and organization
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --claude --organize

# Quick analysis without Claude AI
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --basic

# Enhanced analysis with custom settings
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --claude --sample=30 --confidence=7 --verbose

# Full analysis with file moving and custom config
/analyze-my-photos /Users/carlosmartinez/Documents/2024-09-08 --claude --organize --move --config=config/enhanced_photo_analyzer_config.yaml --verbose
```

### Workflow
1. **Environment Setup** - Source .env file and verify Claude API key
2. **Path Validation** - Verify the directory exists and contains photos
3. **ExifTool Check** - Ensure exiftool is available for enhanced analysis
4. **Claude AI Setup** - Verify Claude API key and connectivity
5. **Output Setup** - Create organized output directory structure
6. **Script Execution** - Run the appropriate Python analysis script
7. **Progress Monitoring** - Track analysis progress and handle errors
8. **Results Summary** - Display analysis results and statistics
9. **Organization** - Organize files if requested

### Python Script Execution
The command automatically runs the appropriate Python scripts:

**Recommended - Quick Analysis with Claude AI:**
```bash
# Source environment and run quick analysis
source .env
python -m src.quick_analyze [directory] --claude --organize
```

**Enhanced Analysis with Claude AI:**
```bash
# Source environment and run enhanced analysis
source .env
python -m src.quick_analyze [directory] --claude --config config/enhanced_photo_analyzer_config.yaml --organize
```

**Legacy Enhanced Analysis:**
```bash
python -m src.cli analyze-exif [directory] /Users/carlosmartinez/Document/GitHub/photo-organizer/output/[directory_name] --organize --move
```

**Basic Analysis:**
```bash
python -m src.cli analyze [directory] /Users/carlosmartinez/Document/GitHub/photo-organizer/output/[directory_name]
```

### Output Structure
The analysis results will be saved to:
```
/Users/carlosmartinez/Document/GitHub/photo-organizer/output/[directory_name]/
├── analysis_summary.txt          # Human-readable summary
├── analysis_summary.json         # Structured data
├── exif_analysis_results.json    # Detailed EXIF analysis
├── organized/                    # Organized photos (if requested)
│   ├── Portrait/
│   ├── Landscape/
│   ├── Event/
│   └── Street/
└── reports/
    └── summary_report.txt
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

### Sample Output
```
📸 Quick Photo Analysis
📁 Source: /Users/carlosmartinez/Documents/2024-09-08
📂 Output: /Users/carlosmartinez/Document/GitHub/photo-organizer/output/analysis
🤖 Claude AI: Enabled
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
  - 20 photos analyzed with Claude AI
  - 3 category overrides applied
  - Average confidence: 8.2/10
  - Content validation: 95% accuracy

📄 Results saved to: /Users/carlosmartinez/Document/GitHub/photo-organizer/output/analysis
```

### Why This Command?
- **🎯 One Command Does Everything**: From basic analysis to full Claude AI integration
- **🚀 Optimized for Your Workflow**: Designed specifically for your directory structure
- **🤖 Smart Defaults**: Intelligent parameter selection based on your needs
- **📊 Comprehensive Results**: Everything you need to know about your photos
- **🔧 Easy to Use**: Simple parameters, clear output, helpful error messages 