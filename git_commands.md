# Git Commands for Law Office Management System

## Initial Setup (First Time)
```bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Law office management system"

# Connect to GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Regular Updates
```bash
# Check status
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit with message
git commit -m "Update: description of changes"

# Push to GitHub
git push
```

## Useful Commands
```bash
# View commit history
git log --oneline

# Check differences
git diff

# Check remote repository
git remote -v

# Pull latest changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name
```

## Recommended Commit Messages
```bash
# For new features
git commit -m "Add: new task management module"

# For bug fixes
git commit -m "Fix: Arabic text rendering issue"

# For updates
git commit -m "Update: improve case search functionality"

# For documentation
git commit -m "Docs: update installation instructions"

# For performance
git commit -m "Optimize: database query performance"
```

## .gitignore Recommendations
Create a .gitignore file to exclude:
```
# Database files (keep structure, ignore data)
data/*.db
data/backups/*.db

# Python cache
__pycache__/
*.pyc
*.pyo

# Virtual environment
venv/
env/

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
```