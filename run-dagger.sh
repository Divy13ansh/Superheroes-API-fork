#!/bin/bash

# Dagger Pipeline Runner for Superheroes API
# Usage: ./run-dagger.sh [pipeline_type]
# pipeline_type: full, quick, security, docker, setup, license

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Dagger Pipeline for Superheroes API${NC}"

# Install Python dependencies for Dagger if needed
if ! python3 -c "import dagger" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dagger-io...${NC}"
    python3 -m pip install dagger-io
fi

# Set required environment variables
export SECRET_KEY=${SECRET_KEY:-"django-insecure-dev-key-for-testing"}

# Determine pipeline type
PIPELINE_TYPE=${1:-"quick"}

echo -e "${GREEN}🔧 Running ${PIPELINE_TYPE} pipeline...${NC}"

# Run the Python pipeline script
python3 dagger_pipeline.py $PIPELINE_TYPE

echo -e "${GREEN}✅ Pipeline completed successfully!${NC}"
