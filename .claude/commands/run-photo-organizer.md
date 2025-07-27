# Run Photo Organizer Command

## Command: `/run-photo-organizer`

### Description
Direct execution of the photo organizer Python scripts with exiftool and Claude AI integration. This command bypasses the need to manually type Python commands and handles all the script invocation automatically.

### Usage
```
/run-photo-organizer [source_dir] [output_dir] [options]
```

### Parameters
- `source_dir`: Directory containing photos to analyze
- `output_dir`: Directory for analysis results
- `--claude`: Enable Claude AI content analysis (recommended)
- `--mode=type`: Analysis mode (basic, enhanced, auto)
- `--config=path`: Custom configuration file path
- `--move`: Move files instead of copying
- `--organize`: Organize photos after analysis
- `--clean`: Clean output directory before analysis
- `--exiftool-check`: Verify exiftool is installed
- `--verbose`: Show detailed output
- `--test`: Run in test mode with sample data

### Examples
```
# Quick analysis with Claude AI (recommended)
/run-photo-organizer /Users/carlosmartinez/Documents/2024-09-08 /Users/carlosmartinez/Document/GitHub/photo-organizer/output/analysis --claude

# Full analysis with Claude AI and organization
/run-photo-organizer /Users/carlosmartinez/Documents/2024-09-08 /Users/carlosmartinez/Document/GitHub/photo-organizer/output/analysis --claude --organize

# Enhanced analysis with custom config
/run-photo-organizer /Users/carlosmartinez/Pictures/Raw /Users/carlosmartinez/Document/GitHub/photo-organizer/output/raw --claude --config=config/enhanced_photo_analyzer_config.yaml --organize

# Basic analysis without Claude AI
/run-photo-organizer /Users/carlosmartinez/Pictures/Events /Users/carlosmartinez/Document/GitHub/photo-organizer/output/events --mode=basic --clean

# Full analysis with file moving
/run-photo-organizer /Users/carlosmartinez/Pictures/Portraits /Users/carlosmartinez/Document/GitHub/photo-organizer/output/portraits --claude --organize --move --verbose
```

### Workflow
1. **Environment Setup** - Source .env file and verify Claude API key
2. **Environment Validation** - Check Python environment and exiftool installation
3. **Claude AI Setup** - Verify Claude API key and connectivity (if --claude)
4. **Parameter Processing** - Parse and validate input parameters
5. **Script Selection** - Choose appropriate Python script based on mode
6. **Execution** - Run the selected Python script with parameters
7. **Monitoring** - Track progress and handle any errors
8. **Results** - Display analysis results and statistics
9. **Cleanup** - Perform any requested cleanup operations

### Python Script Execution
The command automatically invokes the appropriate Python scripts:

**Recommended - Quick Analysis with Claude AI:**
```bash
# Source environment and run quick analysis
source .env
python -m src.quick_analyze [source_dir] --claude --organize
```

**Enhanced Analysis with Claude AI:**
```bash
# Source environment and run enhanced analysis
source .env
python -m src.quick_analyze [source_dir] --claude --config [config_path] --organize
```

**Legacy Enhanced Mode:**
```bash
python -m src.cli analyze-exif [source_dir] [output_dir] --config=[config_path] --organize --move
```

**Basic Mode:**
```bash
python -m src.cli analyze [source_dir] [output_dir]
```

**Direct Script Execution:**
```bash
# Enhanced EXIF analysis with exiftool
python src/analyze_photos_exif.py [source_dir] [output_dir] [config_path]

# Basic analysis without exiftool
python src/analyze_photos.py [source_dir] [output_dir]
```

**ExifTool Verification:**
```bash
# Check if exiftool is installed
which exiftool
exiftool -ver
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
- **Analysis Results**: File counts, categories, and statistics
- **Claude AI Results**: Content-aware categorization and confidence scores
- **Performance Metrics**: Processing time and efficiency data
- **Error Reports**: Any issues encountered during processing
- **Organization Summary**: File organization results (if requested)
- **Next Steps**: Recommendations for follow-up actions
- **ExifTool Status**: Verification of exiftool installation and functionality

### Error Handling
- **ExifTool Missing**: Automatic detection and installation guidance
- **Claude API Issues**: Verification of API key and connectivity
- **Python Dependencies**: Verification and installation of required packages
- **File Permissions**: Handling of permission issues
- **Invalid Paths**: Validation and correction of directory paths
- **Memory Issues**: Handling of large file collections

### Performance Optimization
- **Parallel Processing**: Automatic use of multi-threading for large collections
- **Caching**: Intelligent caching of EXIF data to avoid re-processing
- **Batch Processing**: Efficient handling of large file batches
- **Memory Management**: Streaming processing for very large collections
- **Claude AI Sampling**: Smart sampling keeps processing time reasonable 