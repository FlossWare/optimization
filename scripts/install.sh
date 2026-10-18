#!/bin/bash
# Install optimization from GitHub
set -e
pip install "git+https://github.com/FlossWare/optimization.git"
echo "optimization installed successfully."
python3 -c "from optimization import __version__; print(f'  Version: {__version__}')"
