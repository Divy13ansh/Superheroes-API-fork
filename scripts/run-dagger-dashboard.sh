#!/bin/bash

# Dagger TUI Dashboard Runner for Superheroes API

set -e

echo "============================================================"
echo "📊 SUPERHEROES API - DAGGER TUI DASHBOARD"
echo "============================================================"

# Change to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f "env/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

# Check if Dagger is installed
if ! python3 -c "import dagger" 2>/dev/null; then
    echo "📥 Installing Dagger dependencies..."
    pip3 install -r requirements_dagger.txt
fi

echo ""
echo "🚀 Launching Dagger Pipeline with TUI Dashboard..."
echo "============================================================"

# Simple TUI output - show the raw Dagger output with minimal filtering
filter_tui_output() {
    while IFS= read -r line; do
        # Keep the colorful TUI output but filter out excessive noise
        if [[ "$line" != *"consuming"* ]] && [[ "$line" != *"traces"* ]] && [[ "$line" != *"logs"* ]] && [[ "$line" != *"metrics"* ]]; then
            echo "$line"
        fi
    done
}

# Run the Dagger pipeline with TUI
python3 dagger_pipeline.py 2>&1 | filter_tui_output

echo ""
echo "✅ Dagger TUI Dashboard completed!"
