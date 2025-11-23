#!/usr/bin/env python3
"""
Data Visualization Explorer
Catalog and test all visualization scripts in the repository
"""

import os
import glob
from collections import defaultdict

def categorize_visualizations():
    """Categorize all Python visualization files"""

    categories = defaultdict(list)

    # Get all Python files
    py_files = glob.glob("*.py")
    py_files = [f for f in py_files if f not in ['explore_visualizations.py']]

    for file in sorted(py_files):
        # Categorize based on filename patterns
        if '2D' in file:
            categories['2D Visualizations'].append(file)
        elif '3D' in file:
            categories['3D Visualizations'].append(file)
        elif 'Animation' in file or 'Animated' in file:
            categories['Animations'].append(file)
        elif 'Graph' in file:
            categories['Graphs & Networks'].append(file)
        elif any(term in file for term in ['Voltage', 'Current', 'Resistance', 'Circuit', 'Battery']):
            categories['Electrical Engineering'].append(file)
        elif any(term in file for term in ['Wave', 'Motion', 'Magnetic', 'Electron']):
            categories['Physics'].append(file)
        elif any(term in file for term in ['Trigonometric', 'Integral', 'Derivative', 'Matrix']):
            categories['Mathematics'].append(file)
        else:
            categories['Other'].append(file)

    return categories

def print_catalog():
    """Print a catalog of all visualizations"""

    categories = categorize_visualizations()

    print("=" * 80)
    print("📊 DATA VISUALIZATION CATALOG")
    print("=" * 80)
    print()

    total = 0
    for category, files in sorted(categories.items()):
        print(f"\n{'='*80}")
        print(f"📁 {category} ({len(files)} files)")
        print(f"{'='*80}")

        for i, file in enumerate(files[:10], 1):  # Show first 10
            print(f"  {i:2d}. {file}")

        if len(files) > 10:
            print(f"     ... and {len(files) - 10} more")

        total += len(files)

    print()
    print("=" * 80)
    print(f"📊 TOTAL: {total} visualization scripts")
    print("=" * 80)
    print()
    print("To run a visualization:")
    print("  python <filename.py>")
    print("  OR")
    print("  ./run_visualization.sh <filename.py>")
    print()

def search_visualizations(keyword):
    """Search for visualizations by keyword"""

    py_files = glob.glob("*.py")
    matches = [f for f in py_files if keyword.lower() in f.lower()]

    if matches:
        print(f"\n🔍 Found {len(matches)} matches for '{keyword}':")
        print("=" * 80)
        for i, file in enumerate(matches, 1):
            print(f"  {i}. {file}")
    else:
        print(f"\n❌ No matches found for '{keyword}'")

    return matches

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "search":
        if len(sys.argv) > 2:
            search_visualizations(sys.argv[2])
        else:
            print("Usage: python explore_visualizations.py search <keyword>")
    else:
        print_catalog()
