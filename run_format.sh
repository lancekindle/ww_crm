#!/bin/bash
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Format code using Ruff
echo "Running black formatter..."
# Use Python from the script directory's virtual environment
black --line-length 120 .

echo "Format completed successfully!"
