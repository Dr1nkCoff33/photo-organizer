# Photo Analysis Command

## Command: `/analyze-photos`

### Description
Comprehensive photo analysis and organization workflow that handles the most common use cases for photo processing with Claude AI integration.

### Usage
```
/analyze-photos [source_dir] [output_dir] [options]
```

### Parameters
- `source_dir`: Directory containing photos to analyze
- `output_dir`: Directory for analysis results
- `--claude`: Enable Claude AI content analysis (recommended)
- `--config=path`: Custom configuration file path
- `--move`: Move files instead of copying
- `--quick`: Use basic analysis (faster, less detailed)
- `--full`: Use enhanced EXIF analysis (slower, more detailed)
- `--organize`: Organize photos after analysis
- `--clean`: Clean output directory before analysis

### Examples
```
# Quick analysis with Claude AI (recommended)
/analyze-photos /Users/carlosmartinez/Pictures/Raw /Users/carlosmartinez/Document/GitHub/photo-organizer/output/analysis --claude

# Full analysis with Claude AI and organization
/analyze-photos /Users/carlosmartinez/Pictures/Events /Users/carlosmartinez/Document/GitHub/photo-organizer/output/events --claude --organize

# Enhanced analysis with custom config
/analyze-photos /Users/carlosmartinez/Pictures/Portraits /Users/carlosmartinez/Document/GitHub/photo-organizer/output/portraits --claude --config=config/enhanced_photo_analyzer_config.yaml --organize

# Basic analysis without Claude AI
/analyze-photos /Users/carlosmartinez/Pictures/Events /Users/carlosmartinez/Document/GitHub/photo-organizer/output/events --quick --clean
```

### Workflow
1. **Environment Setup** - Source .env file and verify Claude API key
2. **Validate inputs** - Check source and output directories exist
3. **Claude AI Setup** - Verify Claude API key and connectivity (if --claude)
4. **Setup environment** - Create output directories, load configuration
5. **Run analysis** - Execute appropriate analyzer (basic, enhanced, or Claude AI)
6. **Generate reports** - Create summary reports and statistics
7. **Organize files** - If requested, organize photos by date/category
8. **Cleanup** - Remove temporary files, update progress
9. **Summary** - Display results and next steps

### Python Script Execution
The command will automatically invoke the appropriate Python scripts:

**Recommended - Quick Analysis with Claude AI:**
```bash
# Source environment and run quick analysis
source .env
python -m src.quick_analyze [source_dir] --claude --organize
```

**For Enhanced Analysis with Claude AI (--full --claude):**
```bash
# Source environment and run enhanced analysis
source .env
python -m src.quick_analyze [source_dir] --claude --config [config_path] --organize
```

**For Basic Analysis (--quick):**
```bash
python -m src.cli analyze [source_dir] [output_dir]
```

**Legacy Enhanced Analysis:**
```bash
python -m src.cli analyze-exif [source_dir] [output_dir] [options]
```

### Claude AI Integration
When `--claude` is used:
- **API Key Verification**: Checks for CLAUDE_API_KEY environment variable
- **Sample Analysis**: Analyzes 20 sample photos by default
- **Content Validation**: Validates EXIF-based categorizations
- **Edge Case Handling**: Identifies photos that EXIF alone might miss
- **Confidence Scoring**: Provides confidence levels for each categorization
- **Category Overrides**: Can override EXIF categories with high confidence (8+)

### Output
- **Analysis Summary**: Human-readable summary with emojis and clear formatting
- **JSON Summary**: Structured data for programmatic access
- **Detailed Analysis**: Comprehensive EXIF and Claude AI results
- **Organized Photo Structure**: Category-based organization (if requested)
- **Performance Metrics**: Processing time and efficiency data
- **Claude AI Results**: Content-aware categorization and confidence scores
- **Recommendations**: Suggestions for next steps

### Expected Results
With Claude AI enabled, you'll see:
- **Enhanced Accuracy**: Content-aware categorization
- **Confidence Scores**: Claude AI confidence levels for each category
- **Category Overrides**: High-confidence overrides of EXIF-based categories
- **Edge Case Detection**: Photos that EXIF analysis might miss
- **Sample Analysis**: Results from 20 analyzed photos with detailed insights 