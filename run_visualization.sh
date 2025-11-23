#!/bin/bash
# Helper script to run visualizations in the virtual environment

# Activate virtual environment
source venv/bin/activate

# Check if a filename was provided
if [ $# -eq 0 ]; then
    echo "📊 Data Visualization Runner"
    echo "=============================="
    echo ""
    echo "Usage: ./run_visualization.sh <filename.py>"
    echo ""
    echo "Examples:"
    echo "  ./run_visualization.sh 3D_Display_Mathematical_Calculations.py"
    echo "  ./run_visualization.sh Trigonometric_Relationship.py"
    echo ""
    echo "Available visualizations:"
    ls *.py | head -20
    echo ""
    echo "... and many more!"
else
    echo "🚀 Running: $1"
    python "$1"
fi
