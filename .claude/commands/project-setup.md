---
allowed-tools: Bash, Read, Edit, Grep, Glob
description: Complete project setup and environment configuration for the photo organizer
argument-hint: [--fresh] [--dev] [--exiftool] [--config=path] [--test]
---

# Project Setup Command

## Command: `/setup-project`

### Description
Complete project setup and environment configuration for the photo organizer project.

### Usage
```
/setup-project [options]
```

### Parameters
- `--fresh`: Start with a clean setup (remove existing configs)
- `--dev`: Install development dependencies
- `--exiftool`: Install exiftool automatically
- `--config=path`: Use custom configuration template
- `--test`: Run tests after setup

### Examples
```
/setup-project --fresh --dev
/setup-project --exiftool --test
/setup-project --config=config/production_config.yaml
```

### Workflow
1. **Environment Check** - Verify Python version, system requirements
2. **Dependencies** - Install Python packages from requirements.txt
3. **System Tools** - Install exiftool if requested
4. **Configuration** - Set up default or custom configuration files
5. **Directory Structure** - Create necessary directories
6. **Permissions** - Set appropriate file permissions
7. **Testing** - Run basic tests to verify setup
8. **Documentation** - Generate setup summary

### Python Script Execution
The command will automatically invoke the appropriate Python scripts and system commands:

**For Dependencies:**
```bash
pip install -r requirements.txt
```

**For ExifTool Installation:**
```bash
# macOS
brew install exiftool

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y exiftool

# Or use make
make setup-exiftool
```

**For Testing:**
```bash
python test_enhanced_analyzer.py
python -m src.cli test
```

**For Configuration Setup:**
```bash
# Copy and modify configuration
cp config/photo_analyzer_config.yaml config/custom_config.yaml
```

### Output
- Setup status report
- Installed dependencies list
- Configuration file locations
- Next steps for usage
- Troubleshooting information if needed
