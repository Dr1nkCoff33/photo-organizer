# Photo Organizer Makefile
# Common tasks for development and usage

.PHONY: help install test clean lint format setup-exiftool run-basic run-enhanced run-organize

# Default target
help:
	@echo "Photo Organizer - Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install        - Install Python dependencies"
	@echo "  setup-exiftool - Install exiftool (required for enhanced analysis)"
	@echo ""
	@echo "Development:"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  format         - Format code"
	@echo "  clean          - Clean generated files"
	@echo ""
	@echo "Usage:"
	@echo "  run-basic      - Run basic photo analysis"
	@echo "  run-enhanced   - Run enhanced EXIF analysis"
	@echo "  run-organize   - Organize photos"
	@echo ""
	@echo "Examples:"
	@echo "  make run-enhanced SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output"

# Setup targets
install:
	pip install -r requirements.txt

setup-exiftool:
	@echo "Installing exiftool..."
	@if command -v brew >/dev/null 2>&1; then \
		echo "Using Homebrew to install exiftool..."; \
		brew install exiftool; \
	elif command -v apt-get >/dev/null 2>&1; then \
		echo "Using apt-get to install exiftool..."; \
		sudo apt-get update && sudo apt-get install -y exiftool; \
	elif command -v yum >/dev/null 2>&1; then \
		echo "Using yum to install exiftool..."; \
		sudo yum install -y exiftool; \
	else \
		echo "Please install exiftool manually from https://exiftool.org/"; \
		exit 1; \
	fi
	@echo "exiftool installation completed!"

# Development targets
test:
	python -m pytest test_enhanced_analyzer.py -v

lint:
	@echo "Running flake8..."
	flake8 src/ --max-line-length=100 --ignore=E203,W503
	@echo "Running mypy..."
	mypy src/ --ignore-missing-imports

format:
	black src/ --line-length=100
	isort src/

clean:
	@echo "Cleaning generated files..."
	rm -rf output/analysis/*
	rm -rf output/exif_analysis/*
	rm -rf output/organized/*
	rm -rf output/reports/*
	rm -rf output/temp/*
	rm -rf output/temporal_chunks/*
	rm -rf output/conversations_by_topic/*
	rm -rf output/exports/*
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleanup completed!"

# Usage targets
run-basic:
	@if [ -z "$(SOURCE_DIR)" ] || [ -z "$(OUTPUT_DIR)" ]; then \
		echo "Usage: make run-basic SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output"; \
		exit 1; \
	fi
	python -m src.cli analyze "$(SOURCE_DIR)" "$(OUTPUT_DIR)"

run-enhanced:
	@if [ -z "$(SOURCE_DIR)" ] || [ -z "$(OUTPUT_DIR)" ]; then \
		echo "Usage: make run-enhanced SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output"; \
		exit 1; \
	fi
	python -m src.cli analyze-exif "$(SOURCE_DIR)" "$(OUTPUT_DIR)"

run-organize:
	@if [ -z "$(SOURCE_DIR)" ] || [ -z "$(OUTPUT_DIR)" ]; then \
		echo "Usage: make run-organize SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output"; \
		exit 1; \
	fi
	python -m src.cli organize "$(SOURCE_DIR)" "$(OUTPUT_DIR)"

# Quick test with sample data
test-quick:
	@echo "Running quick test..."
	@if [ -d "data/raw" ]; then \
		python -m src.cli analyze-exif data/raw output/test_analysis; \
	else \
		echo "No test data found in data/raw/"; \
		echo "Please add some photo files to data/raw/ for testing"; \
	fi

# Install development dependencies
install-dev: install
	pip install flake8 black isort mypy pytest

# Full setup
setup: install setup-exiftool
	@echo "Full setup completed!"
	@echo "You can now use the photo organizer with:"
	@echo "  make run-enhanced SOURCE_DIR=/path/to/photos OUTPUT_DIR=/path/to/output" 