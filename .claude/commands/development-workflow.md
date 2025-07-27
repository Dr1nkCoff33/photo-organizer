# Development Workflow Command

## Command: `/dev-workflow`

### Description
Comprehensive development workflow management for the photo organizer project.

### Usage
```
/dev-workflow [action] [options]
```

### Actions
- `test`: Run all tests
- `lint`: Run code linting and style checks
- `format`: Format code with black and isort
- `clean`: Clean generated files and caches
- `build`: Build package for distribution
- `docs`: Generate documentation
- `all`: Run test, lint, and format in sequence

### Parameters
- `--verbose`: Show detailed output
- `--fix`: Auto-fix issues where possible
- `--coverage`: Generate test coverage report
- `--quick`: Skip slow tests
- `--output=path`: Specify output directory for reports

### Examples
```
/dev-workflow test --coverage
/dev-workflow lint --fix
/dev-workflow format
/dev-workflow all --verbose
/dev-workflow clean --output=output/reports
```

### Workflow
1. **Action Selection** - Determine which development task to run
2. **Environment Check** - Verify development environment is ready
3. **Execute Task** - Run the specified action with options
4. **Generate Reports** - Create reports and summaries
5. **Display Results** - Show results and recommendations
6. **Next Steps** - Suggest follow-up actions

### Python Script Execution
The command will automatically invoke the appropriate Python scripts and tools:

**For Testing:**
```bash
python -m pytest test_enhanced_analyzer.py -v
python test_enhanced_analyzer.py
```

**For Linting:**
```bash
flake8 src/ --max-line-length=100 --ignore=E203,W503
mypy src/ --ignore-missing-imports
```

**For Formatting:**
```bash
black src/ --line-length=100
isort src/
```

**For Cleaning:**
```bash
make clean
```

**For Building:**
```bash
python setup.py build
```

### Output
- Task execution status
- Performance metrics
- Issues found and fixes applied
- Recommendations for improvement
- Generated reports and artifacts 