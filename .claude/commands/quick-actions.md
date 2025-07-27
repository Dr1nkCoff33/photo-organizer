# Quick Actions Command

## Command: `/quick`

### Description
Quick access to common tasks and shortcuts for the photo organizer project.

### Usage
```
/quick [action] [options]
```

### Actions
- `analyze`: Quick photo analysis (basic mode)
- `organize`: Quick photo organization
- `test`: Quick test run
- `clean`: Quick cleanup
- `status`: Quick project status
- `help`: Show available quick actions
- `config`: Quick configuration check
- `backup`: Quick backup of important files

### Parameters
- `--source=path`: Source directory for photo operations
- `--output=path`: Output directory for results
- `--force`: Skip confirmations
- `--verbose`: Show detailed output

### Examples
```
/quick analyze --source=/Users/carlosmartinez/Pictures --output=output/quick
/quick organize --source=/Users/carlosmartinez/Pictures/Raw --force
/quick test --verbose
/quick status
/quick backup
```

### Workflow
1. **Action Selection** - Determine which quick action to perform
2. **Parameter Processing** - Handle source/output paths and options
3. **Validation** - Quick validation of inputs and environment
4. **Execution** - Run the action with minimal overhead
5. **Summary** - Provide quick results and status

### Python Script Execution
The command will automatically invoke the appropriate Python scripts:

**For Quick Analysis:**
```bash
python -m src.cli analyze-exif [source_dir] [output_dir] --quick
```

**For Quick Organization:**
```bash
python -m src.cli organize [source_dir] [output_dir] --move
```

**For Quick Test:**
```bash
python test_enhanced_analyzer.py
```

**For Quick Cleanup:**
```bash
make clean
```

### Output
- Quick execution status
- Basic results summary
- Time taken for operation
- Any immediate issues or warnings
- Suggested next steps 