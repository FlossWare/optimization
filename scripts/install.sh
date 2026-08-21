#!/bin/bash
# Install genetic-optimizer-ai from GitHub
set -e
pip install "git+https://github.com/FlossWare/genetic-optimizer-ai.git"
echo "genetic-optimizer-ai installed successfully."
python3 -c "from genetic_optimizer_ai import __version__; print(f'  Version: {__version__}')"
