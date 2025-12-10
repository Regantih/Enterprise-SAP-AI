#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set PYTHONPATH to the project root
export PYTHONPATH="$SCRIPT_DIR"

# Define the Python executable from the virtual environment
PYTHON_EXEC="$SCRIPT_DIR/spark-lab/bin/python3"

# Check if the virtual environment python exists, fallback to system python if not
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "⚠️  Virtual environment not found at $PYTHON_EXEC. Using system python3."
    PYTHON_EXEC="python3"
fi

# Clear screen
clear

echo "========================================================"
echo "   🏛️  ATHENA AGENTIC SYSTEM - INTERACTIVE DEMO  🏛️"
echo "========================================================"
echo "Select a demo scenario to run:"
echo ""

PS3='Please enter your choice (1-4): '
options=("Run Research Agent (Knowledge Arbitrage)" "Run Deployment Simulation (SAP AI Core)" "Show Quality Dashboard (Observability)" "Launch Web UI (Interactive Chat)" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Run Research Agent (Knowledge Arbitrage)")
            echo ""
            echo "🚀 Launching Apollo & Clio Agents..."
            echo "-----------------------------------"
            "$PYTHON_EXEC" -m athena_system.workflows.knowledge_arbitrage --topic "Agentic AI"
            echo ""
            echo "✅ Demo Complete. Press Enter to continue."
            read
            ;;
        "Run Deployment Simulation (SAP AI Core)")
            echo ""
            echo "🚀 Launching Deployment Simulator..."
            echo "-----------------------------------"
            "$PYTHON_EXEC" -m athena_system.deployment.deploy
            echo ""
            echo "✅ Demo Complete. Press Enter to continue."
            read
            ;;
        "Show Quality Dashboard (Observability)")
            echo ""
            echo "📊 Launching Quality Dashboard..."
            echo "-----------------------------------"
            "$PYTHON_EXEC" -m athena_system.utils.quality_dashboard
            echo ""
            echo "✅ Demo Complete. Press Enter to continue."
            read
            ;;
        "Launch Web UI (Interactive Chat)")
            echo ""
            echo "🌐 Launching Web UI..."
            echo "-----------------------------------"
            echo "Open http://localhost:8000 in your browser."
            echo "Press Ctrl+C to stop the server and return to menu."
            "$PYTHON_EXEC" -m athena_system.web_ui.server
            ;;
        "Quit")
            echo "Exiting..."
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
    
    # Re-print menu
    clear
    echo "========================================================"
    echo "   🏛️  ATHENA AGENTIC SYSTEM - INTERACTIVE DEMO  🏛️"
    echo "========================================================"
    echo "Select a demo scenario to run:"
    echo ""
    REPLY=
done
