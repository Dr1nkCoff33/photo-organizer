# Photo Organizer

Python-based RAW photo organization and analysis tool for photographers.

## Features

- **RAW Photo Analysis**: Automated analysis of RAW photo files
- **Date-based Organization**: Intelligent sorting by capture date
- **Burst Detection**: Automatic detection and grouping of photo sequences
- **Content Categorization**: Smart categorization based on photo content
- **Batch Processing**: Efficient processing of large photo collections

## Project Structure

```
photo-organizer/
├── src/                          # Source code
│   ├── analyze_photos.py         # Basic photo analysis script
│   ├── analyze_photos_exif.py    # Enhanced EXIF analyzer
│   ├── cli.py                    # Command-line interface
│   └── utils/                    # Utility functions
│       ├── file_utils.py         # File operations
│       ├── exif_utils.py         # EXIF data handling
│       └── date_utils.py         # Date processing
├── config/                       # Configuration files
│   └── photo_analyzer_config.yaml
├── data/                         # Photo data storage
│   ├── raw/                      # Raw photo files
│   └── processed/                # Processed photo data
├── output/                       # Analysis outputs
│   ├── analysis/                 # Analysis reports
│   ├── exif_analysis/            # EXIF analysis results
│   ├── organized/                # Organized photo collections
│   └── reports/                  # General reports
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
├── Makefile                      # Development tasks
├── config.py                     # Main configuration
└── README.md                     # Project documentation
```

## Installation

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/photo-organizer.git
cd photo-organizer

# Full setup (installs dependencies and exiftool)
make setup
```

### Manual Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/photo-organizer.git
cd photo-organizer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install exiftool (required for enhanced analysis):
```bash
# macOS
brew install exiftool

# Ubuntu/Debian
sudo apt-get install exiftool

# Or use the make command
make setup-exiftool
```

4. Set up configuration:
```bash
# Edit the configuration file as needed
nano config/photo_analyzer_config.yaml
```

## Usage

### Command Line Interface

The photo organizer provides a convenient CLI for all operations:

```bash
# Show help
python -m src.cli --help

# Basic photo analysis
python -m src.cli analyze /path/to/photos /path/to/output

# Enhanced EXIF analysis
python -m src.cli analyze-exif /path/to/photos /path/to/output

# Organize photos by date and category
python -m src.cli organize /path/to/photos /path/to/output --move

# Use custom configuration
python -m src.cli analyze-exif /path/to/photos /path/to/output --config config/custom.yaml
```

### Using Make Commands

For convenience, you can use the provided Makefile:

```bash
# Show available commands
make help

# Run enhanced analysis
make run-enhanced SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output

# Run organization
make run-organize SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output

# Quick test with sample data
make test-quick
```

### Python API

```python
from src.analyze_photos_exif import main, PhotoAnalyzerConfig

# Load custom configuration
config = PhotoAnalyzerConfig('config/photo_analyzer_config.yaml')

# Run analysis
result = main('/path/to/photos', '/path/to/output', 'config/photo_analyzer_config.yaml')
```

## Features

### Photo Analysis
- **File Information**: Extract metadata, dates, and file properties
- **Sequence Detection**: Identify burst shots and photo sequences
- **Content Analysis**: Analyze photo content for categorization

### Organization
- **Date-based Sorting**: Organize by capture date
- **Burst Grouping**: Group related photos together
- **Category Classification**: Sort by content type

### Output Formats
- **JSON Reports**: Detailed analysis reports
- **Organized Folders**: Structured photo collections
- **Summary Statistics**: Overview of photo collection

## Dependencies

- Python 3.8+
- PIL/Pillow for image processing
- ExifRead for metadata extraction
- pandas for data analysis
- numpy for numerical operations

## Configuration

Edit `config.py` to customize:
- File type filters
- Date format preferences
- Output directory structure
- Analysis parameters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License 