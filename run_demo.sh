#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set PYTHONPATH to the project root
export PYTHONPATH="$SCRIPT_DIR"

echo "🚀 Athena System: Launching Deployment Demo..."
echo "📂 Project Root: $SCRIPT_DIR"
echo "---------------------------------------------"

# Run the deployment script using the virtual environment python
"$SCRIPT_DIR/spark-lab/bin/python3" -m athena_system.deployment.deploy
