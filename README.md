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
├── src/                    # Source code
│   ├── analyze_photos.py   # Main photo analysis script
│   ├── photo_processor.py  # Photo processing utilities
│   └── utils/              # Utility functions
├── data/                   # Photo data
│   ├── raw/                # Raw photo files
│   └── processed/          # Processed photo data
├── output/                 # Analysis outputs
│   ├── reports/            # Analysis reports
│   └── organized/          # Organized photo collections
├── requirements.txt
├── config.py
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/photo-organizer.git
cd photo-organizer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
```bash
cp config.py.example config.py
# Edit config.py with your preferences
```

## Usage

### Basic Photo Analysis

```bash
# Analyze photos in a directory
python src/analyze_photos.py --input-dir /path/to/photos --output-dir /path/to/output

# Analyze specific file types
python src/analyze_photos.py --input-dir /path/to/photos --file-types ARW,CR2,NEF
```

### Batch Processing

```bash
# Process multiple directories
python src/analyze_photos.py --batch-file directories.txt

# Process with specific options
python src/analyze_photos.py --input-dir /path/to/photos --organize-by-date --detect-bursts
```

### Python API

```python
from src.analyze_photos import analyze_photo_sequence, categorize_photos

# Analyze photo sequence
bursts = analyze_photo_sequence(photos)

# Categorize photos
categories = categorize_photos(photos)
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