# Git Flow Action

Automates git commits and pushes with configurable commit messages and branch selection.

## Usage

```bash
claude run git-flow-action
```

## Features

- Manual trigger via workflow dispatch with customizable commit message and branch
- Automatic trigger on pushes to main/develop branches (excluding .md and .github files)
- Configures git with GitHub Action bot credentials
- Adds all changes to staging
- Checks for changes before committing
- Commits with specified or default message
- Pushes to specified branch

## GitHub Action Configuration

Create `.github/workflows/auto-commit-push.yml`:

```yaml
name: Auto Commit and Push

on:
  workflow_dispatch:
    inputs:
      commit_message:
        description: 'Commit message'
        required: true
        default: 'Auto commit changes'
      branch:
        description: 'Branch to push to'
        required: true
        default: 'main'
  push:
    branches: [ main, develop ]
    paths-ignore:
      - '**.md'
      - '.github/**'

jobs:
  auto-commit-push:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Configure Git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
    
    - name: Add all changes
      run: |
        git add .
        echo "Added all changes to staging"
    
    - name: Check for changes
      id: check_changes
      run: |
        if [[ -n "$(git status --porcelain)" ]]; then
          echo "has_changes=true" >> $GITHUB_OUTPUT
          echo "Changes detected, proceeding with commit"
        else
          echo "has_changes=false" >> $GITHUB_OUTPUT
          echo "No changes to commit"
        fi
    
    - name: Commit changes
      if: steps.check_changes.outputs.has_changes == 'true'
      run: |
        git commit -m "${{ github.event.inputs.commit_message || 'Auto commit changes' }}"
        echo "Committed changes"
    
    - name: Push changes
      if: steps.check_changes.outputs.has_changes == 'true'
      run: |
        git push origin ${{ github.event.inputs.branch || 'main' }}
        echo "Pushed changes to ${{ github.event.inputs.branch || 'main' }}"
    
    - name: No changes message
      if: steps.check_changes.outputs.has_changes == 'false'
      run: |
        echo "No changes to commit or push"
```

## Setup Instructions

1. Create the `.github/workflows` directory if it doesn't exist
2. Copy the above YAML content into `.github/workflows/auto-commit-push.yml`
3. Commit and push to your repository
4. The action will be available in the "Actions" tab of your GitHub repository

## Triggering the Workflow

### Manual Trigger
1. Go to Actions tab in your GitHub repository
2. Select "Auto Commit and Push" workflow
3. Click "Run workflow"
4. Enter commit message and target branch
5. Click "Run workflow" button

### Automatic Trigger
The workflow automatically runs when:
- Pushing to `main` or `develop` branches
- Changes are not in `.md` files or `.github/` directory

## Notes

- Uses GitHub's default GITHUB_TOKEN for authentication
- Commits are made with "GitHub Action" as the author
- Only commits if there are actual changes
- Provides clear console output for each step