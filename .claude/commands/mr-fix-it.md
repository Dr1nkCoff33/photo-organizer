---
allowed-tools: Bash, Read, Edit, Grep, Glob, Search
description: Fix YAML frontmatter and Markdown file formatting issues
argument-hint: [file_or_directory] [--validate] [--format] [--fix-all] [--backup]
---

## Context

- Current directory: !`pwd`
- Target files: !`if [ -n "$ARGUMENTS" ]; then echo "Target: $ARGUMENTS"; else echo "Target: Current directory"; fi`
- Markdown files found: !`find . -name "*.md" -type f | wc -l`
- YAML files found: !`find . -name "*.yml" -o -name "*.yaml" | wc -l`

## Your Task

Fix YAML frontmatter and Markdown file formatting issues. This command can validate, format, and repair common problems in YAML frontmatter and Markdown content.

**Parameters:**
- File/Directory: $ARGUMENTS (default: current directory)
- Validation mode: Check for --validate flag
- Format mode: Check for --format flag
- Fix all issues: Check for --fix-all flag
- Create backups: Check for --backup flag

**Common Issues to Fix:**

### YAML Frontmatter Issues:
1. **Missing or malformed YAML delimiters** (`---`)
2. **Incorrect indentation** (should use 2 spaces)
3. **Invalid YAML syntax** (quotes, special characters)
4. **Missing required fields** (description, allowed-tools, etc.)
5. **Inconsistent formatting** (spacing, line breaks)

### Markdown Issues:
1. **Broken links and references**
2. **Inconsistent heading levels**
3. **Malformed code blocks**
4. **Missing or incorrect file references** (`@filename`)
5. **Invalid bash command syntax** (`!command`)
6. **Trailing whitespace and formatting**

**Workflow:**
1. **Scan and Identify**: Find all Markdown and YAML files in target
2. **Validate Structure**: Check YAML frontmatter syntax and Markdown formatting
3. **Detect Issues**: Identify specific problems in each file
4. **Create Backups**: If --backup flag is set, create backup copies
5. **Apply Fixes**:
   - Fix YAML syntax errors
   - Standardize frontmatter structure
   - Correct Markdown formatting
   - Validate file references and bash commands
6. **Report Results**: Show what was fixed and any remaining issues

**Validation Checks:**
- YAML syntax validation using `yamllint` or similar
- Markdown link validation
- File reference existence checks
- Bash command syntax validation
- Frontmatter completeness check

**Expected Output:**
- List of files processed
- Specific issues found and fixed
- Validation results
- Backup file locations (if created)
- Summary of changes made
- Any remaining issues that need manual attention

**Safety Features:**
- Always create backups when making changes (if --backup flag)
- Validate YAML syntax before applying changes
- Check file references exist before updating
- Preserve original formatting where possible
- Show diff of changes before applying

Focus on maintaining file integrity while fixing formatting issues. Provide clear explanations of what was changed and why.
