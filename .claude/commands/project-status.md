# Project Status Command

## Command: `/project-status`

### Description
Comprehensive project status and health check for the photo organizer project.

### Usage
```
/project-status [options]
```

### Parameters
- `--detailed`: Show detailed analysis
- `--health`: Focus on project health issues
- `--performance`: Show performance metrics
- `--files`: Show file structure analysis
- `--dependencies`: Check dependency status
- `--config`: Validate configuration files
- `--all`: Show all status information

### Examples
```
/project-status --detailed
/project-status --health --performance
/project-status --files --config
/project-status --all
```

### Workflow
1. **Project Structure** - Analyze directory structure and file organization
2. **Code Quality** - Check code metrics, complexity, and coverage
3. **Dependencies** - Verify package versions and compatibility
4. **Configuration** - Validate configuration files and settings
5. **Performance** - Analyze performance bottlenecks and optimizations
6. **Documentation** - Check documentation completeness
7. **Testing** - Verify test coverage and quality
8. **Recommendations** - Provide actionable improvement suggestions

### Output
- Project health score (0-100)
- File structure analysis
- Code quality metrics
- Dependency status
- Configuration validation
- Performance analysis
- Documentation status
- Test coverage report
- Priority recommendations
- Action items for improvement 