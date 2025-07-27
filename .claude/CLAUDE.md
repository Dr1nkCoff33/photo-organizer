# Claude Configuration for Photo Organizer

## Default Behavior
- Always prompt for input and output directories
- Never save output files inside the repository
- Ask for Claude AI sample size when --claude flag is used
- Use external directories for all photo storage and analysis results

## Available Commands
- `/analyze-my-photos` - Main photo analysis command with EXIF and Claude AI
- `/claude-photo-analysis` - Direct Claude AI photo analysis
- `/project-setup` - Setup and configuration help

## Key Directories
- **src/**: Source code for analysis scripts
- **config/**: Configuration files (YAML)
- **.claude/**: Command definitions and settings
- **NO output/** directory - all outputs go to user-specified locations

## Interactive Prompts
When running commands without full parameters:
1. Ask for photo source directory
2. Ask for output directory  
3. Ask for Claude AI sample size (if using --claude)
4. Confirm settings before proceeding

## Analysis Options
- EXIF-based categorization (default)
- Claude AI content validation (optional)
- Burst sequence detection
- Date-based organization
- Category-based sorting

## Output Standards
- Save all files to user-specified directories
- Never commit photos or analysis results to git
- Use clear folder structure: Category/YYYY-MM/filename
- Generate both human-readable and JSON summaries