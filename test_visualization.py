#!/usr/bin/env python3
"""
Test script to verify visualization environment works
Saves output to PNG file instead of displaying
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("🧪 Testing visualization environment...")

# Create a simple 3D visualization
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create surface plot
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Test Visualization: Z = sin(√(X² + Y²))')

# Add colorbar
fig.colorbar(surf, shrink=0.5, aspect=5)

# Save to file
output_file = 'test_output.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ Visualization saved to: {output_file}")

# Test other libraries
print("\n📦 Checking installed packages:")
import pandas as pd
import plotly
import sympy
import scipy
import networkx

print(f"  ✓ NumPy: {np.__version__}")
print(f"  ✓ Matplotlib: {matplotlib.__version__}")
print(f"  ✓ Pandas: {pd.__version__}")
print(f"  ✓ Plotly: {plotly.__version__}")
print(f"  ✓ SymPy: {sympy.__version__}")
print(f"  ✓ SciPy: {scipy.__version__}")
print(f"  ✓ NetworkX: {networkx.__version__}")

print("\n✅ All packages working correctly!")
print(f"\n💡 To view the test image: open {output_file}")
