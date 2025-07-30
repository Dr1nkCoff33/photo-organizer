# Claude Configuration for Photo Organizer

## Default Behavior
- Always prompt for input and output directories if not provided
- Never save output files inside the repository
- Use enhanced mode by default for balanced speed/accuracy
- Ask for Claude AI sample size when claude mode is selected
- Use external directories for all photo storage and analysis results

## Available Commands
- `/photo-analyze` - Unified photo analysis command with three modes
- `/project-setup` - Setup and configuration help
- `/git-flow-action` - Automated git commits and pushes
- `/mr-fix-it` - YAML and Markdown maintenance tool

## Key Directories
- **.claude/commands/**: Command definitions
- **.claude/agents/**: Agent specifications
- **NO output/** directory - all outputs go to user-specified locations
- **NO src/** directory - all logic handled by agents

## Interactive Prompts
When running commands without full parameters:
1. Ask for photo source directory
2. Ask for output directory
3. Ask for analysis mode (if not specified)
4. Ask for Claude AI sample size (if using claude mode)
5. Confirm settings before proceeding

## Analysis Modes
- **Quick**: Basic EXIF analysis only
- **Enhanced**: Full EXIF + burst detection (default)
- **Claude**: Enhanced + AI content validation

## Organization Options
- Date-based folder structure (YYYY/MM)
- Category-based sorting
- Copy or move operations
- Preserve original metadata

## Output Standards
- Save all files to user-specified directories
- Never commit photos or analysis results to git
- Use clear folder structure: Category/YYYY-MM/filename
- Generate both human-readable and JSON summaries