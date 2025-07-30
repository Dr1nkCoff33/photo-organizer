---
allowed-tools: Bash, Read, Edit, Grep, Glob
description: Analyze photos using Claude AI for content-aware categorization combined with EXIF data
argument-hint: [directory] [--sample=N] [--confidence=N] [--organize] [--verbose]
---

## Context

- Current directory: !`pwd`
- Available photos: !`find $ARGUMENTS -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.arw" -o -iname "*.nef" -o -iname "*.cr2" \) | head -20`
- Environment setup: !`test -f .env && echo "✅ .env file found" || echo "❌ .env file missing"`

## Your Task

Analyze photos in the specified directory using Claude AI for content-aware categorization. Combine EXIF metadata analysis with Claude's visual content analysis for the most accurate photo organization.

**Parameters:**
- Directory: $ARGUMENTS
- Sample size: Extract from --sample=N (default: 20)
- Confidence threshold: Extract from --confidence=N (default: 8)
- Organize files: Check for --organize flag
- Verbose output: Check for --verbose flag

**Workflow:**
1. Validate the source directory and environment setup
2. Run EXIF-based categorization as baseline
3. Select photos for Claude AI analysis (prioritize uncategorized)
4. Use Claude AI to analyze photo content and validate categories
5. Apply high-confidence overrides to EXIF-based categories
6. Generate comprehensive analysis report
7. Organize files if requested

**Expected Output:**
- Categorization breakdown with confidence scores
- Category overrides applied by Claude AI
- Content descriptions for analyzed photos
- Performance metrics and cost considerations
- Organized file structure if requested

Focus on accuracy and provide clear explanations of Claude AI's analysis decisions.
