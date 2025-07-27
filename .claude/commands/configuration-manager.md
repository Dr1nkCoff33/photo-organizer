# Configuration Manager Command

## Command: `/config`

### Description
Comprehensive configuration management for the photo organizer project.

### Usage
```
/config [action] [options]
```

### Actions
- `show`: Display current configuration
- `validate`: Validate configuration files
- `create`: Create new configuration file
- `edit`: Edit existing configuration
- `backup`: Backup current configuration
- `restore`: Restore configuration from backup
- `diff`: Show differences between configurations
- `template`: Generate configuration template
- `reset`: Reset to default configuration

### Parameters
- `--file=path`: Specify configuration file path
- `--section=name`: Focus on specific configuration section
- `--format=type`: Output format (json, yaml, table)
- `--backup-dir=path`: Backup directory location
- `--force`: Skip confirmations

### Examples
```
/config show --format=table
/config validate --file=config/custom.yaml
/config create --template=production
/config edit --section=categories
/config backup --backup-dir=config/backups
/config diff config/default.yaml config/custom.yaml
```

### Workflow
1. **Action Selection** - Determine configuration operation
2. **File Handling** - Load, validate, or create configuration files
3. **Validation** - Check configuration syntax and logic
4. **Processing** - Execute the requested configuration action
5. **Backup** - Create backups if modifying configurations
6. **Summary** - Display results and changes made

### Output
- Configuration status and validation results
- File operations performed
- Configuration differences (if comparing)
- Backup locations and timestamps
- Recommendations for configuration improvements
- Error messages for invalid configurations 