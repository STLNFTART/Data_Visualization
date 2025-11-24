# CLAUDE.md - Data Visualization Repository Guide

## Repository Overview

This repository contains **1000+ Python scripts** focused on mathematical, scientific, and physics data visualizations. The codebase specializes in creating 2D and 3D visualizations for educational and analytical purposes across multiple domains including:

- **Mathematics**: Trigonometry, calculus, linear algebra, graph theory, statistics
- **Physics**: Electromagnetism, circuits, mechanics, wave theory, quantum mechanics
- **Electrical Engineering**: Circuit analysis, AC/DC circuits, power dissipation, resistance calculations
- **Statistics & Probability**: Confidence intervals, distributions, regression analysis
- **Discrete Mathematics**: Graph theory, set theory, Boolean algebra, combinatorics

## Codebase Structure

### Repository Layout

```
Data_Visualization/
├── .git/                    # Git repository metadata
├── README.md                # Basic repository description
├── CLAUDE.md                # This file - AI assistant guide
└── *.py                     # 1000+ Python visualization scripts (flat structure)
```

**Important**: This repository uses a **flat file structure** with all Python files in the root directory. There are no subdirectories for organization.

### File Naming Conventions

Files follow descriptive naming patterns that indicate:

1. **Dimensionality Prefix**:
   - `2D_*.py` - Two-dimensional visualizations
   - `3D_*.py` - Three-dimensional visualizations
   - `01.*.py`, `001.*.py`, `0001.*.py` - Numbered series/variations

2. **Content Description**:
   - Names are highly descriptive, e.g., `3D_Current_vs_EMF_and_Terminal_Voltage.py`
   - Use underscores for word separation
   - Indicate the subject matter directly in filename

3. **Common Patterns**:
   - `Animation_*` - Files with animated visualizations
   - `Interactive_*` - Files with interactive elements
   - `Creative_*` - Files with artistic/creative visualization approaches
   - `Visualization_*` - General visualization scripts

### Examples:
```
3D_Electron_Motion_in_Magnetic_Field.py
2D_Graph_Taylor_Series_Expansion_of_ln(1+x).py
Animation_3D_Mathematical_Dance_of_Sine_and_Cosine.py
Interactive_3D_Scatter_Plot_visualization_$Z=X^2-Y^2$.py
```

## Technology Stack

### Core Dependencies

Based on import analysis, the repository uses:

| Library | Usage Count | Purpose |
|---------|-------------|---------|
| `numpy` | ~933 | Numerical computations, arrays, mathematical operations |
| `matplotlib.pyplot` | ~580 | Static 2D/3D plotting, animations |
| `pandas` | ~490 | Data manipulation and structured data handling |
| `plotly.graph_objects` | ~373 | Interactive 3D visualizations |
| `sympy` | ~331 | Symbolic mathematics, equation solving |
| `plotly.express` | ~296 | Quick interactive plots |
| `mpl_toolkits.mplot3d.Axes3D` | ~291 | 3D plotting with matplotlib |
| `networkx` | ~27 | Graph theory visualizations |
| `torch` | ~34 | Machine learning/tensor operations |
| `sklearn` | ~24 | Statistical modeling (primarily LinearRegression) |
| `scipy.stats` | ~21 | Statistical functions |

### Typical Import Pattern

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sympy as sp
```

### Animation & Interactivity

- `matplotlib.animation.FuncAnimation` - For matplotlib animations
- `ipywidgets` - For Jupyter notebook interactivity
- `plotly` animations - Built-in animation frames

## Code Patterns & Conventions

### Standard Visualization Structure

Most files follow this pattern:

```python
# 1. Imports
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 2. Define parameters/constants
variable = value

# 3. Perform calculations
result = calculation(variable)

# 4. Create visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# 5. Labels and formatting
plt.title('Description')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 6. Display
plt.show()

# 7. Print results (optional)
print(f"Result: {result}")
```

### Plotly Pattern

```python
import plotly.graph_objects as go
import numpy as np

# Create data
x, y, z = create_data()

# Create figure
fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=5, color=z, colorscale='Viridis')
)])

# Update layout
fig.update_layout(
    title='3D Visualization',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig.show()
```

### Common Mathematical Operations

- **Symbolic Math**: Use `sympy` for exact symbolic calculations
- **Numerical Arrays**: Use `numpy` for efficient array operations
- **Mesh Grids**: `np.meshgrid()` for 3D surface plots
- **Linspace**: `np.linspace()` for creating evenly spaced values

## Development Workflows

### Adding New Visualizations

1. **File Naming**: Follow the established convention
   - Start with dimensionality: `2D_` or `3D_`
   - Use descriptive name: `Subject_Matter_Description.py`
   - Add prefixes if needed: `Animation_`, `Interactive_`, `Creative_`

2. **Code Structure**:
   - Import all required libraries at the top
   - Define constants and parameters
   - Perform calculations
   - Create visualizations
   - Add labels, titles, and legends
   - Display results

3. **Documentation**:
   - Use descriptive variable names
   - Add comments for complex calculations
   - Include mathematical formulas in comments when relevant

### Git Workflow

**Branch Naming**: All development branches should follow this pattern:
```
claude/claude-md-{identifier}-{session-id}
```

**Current Working Branch**: `claude/claude-md-micf511gngvbu23v-01CXGFSWju7DKwSYYvEwyCuN`

**Git Commands**:
```bash
# Check status
git status

# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "Add: 3D visualization for [specific topic]"

# Push to current branch
git push -u origin claude/claude-md-micf511gngvbu23v-01CXGFSWju7DKwSYYvEwyCuN
```

**Commit Message Conventions**:
- `Add:` - New visualization script
- `Update:` - Modifications to existing script
- `Fix:` - Bug fixes or corrections
- `Refactor:` - Code improvements without functionality change
- `Docs:` - Documentation updates

## Key Conventions for AI Assistants

### File Operations

1. **Reading Files**:
   - Always use absolute paths
   - Files are in `/home/user/Data_Visualization/`
   - No subdirectories exist

2. **Creating New Files**:
   - Follow naming conventions strictly
   - Place in repository root
   - Avoid creating duplicates

3. **Modifying Files**:
   - Read file first before editing
   - Preserve existing code structure
   - Maintain import patterns

### Code Style Guidelines

1. **Imports**:
   - Standard library first
   - Third-party libraries second
   - Use conventional aliases (`np`, `plt`, `pd`, `go`, `sp`)

2. **Variables**:
   - Use descriptive names
   - Follow snake_case convention
   - Use meaningful mathematical symbols when appropriate

3. **Visualization**:
   - Always include titles, labels, and legends
   - Use appropriate colormaps (`viridis`, `plasma`, `coolwarm`)
   - Set figure size for readability when needed

4. **Comments**:
   - Explain mathematical concepts
   - Document formulas and equations
   - Clarify physical principles when relevant

### Common Tasks

#### Creating a 3D Matplotlib Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create data
x = np.linspace(start, end, points)
y = np.linspace(start, end, points)
X, Y = np.meshgrid(x, y)
Z = function(X, Y)

# Create figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

# Labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('Title')

# Colorbar
fig.colorbar(surf, shrink=0.5)

plt.show()
```

#### Creating an Interactive Plotly Visualization

```python
import plotly.graph_objects as go
import numpy as np

# Create data
x = np.linspace(start, end, points)
y = np.linspace(start, end, points)
X, Y = np.meshgrid(x, y)
Z = function(X, Y)

# Create figure
fig = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z,
    colorscale='Viridis',
    showscale=True
)])

# Update layout
fig.update_layout(
    title='Title',
    scene=dict(
        xaxis_title='X Label',
        yaxis_title='Y Label',
        zaxis_title='Z Label',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    width=800,
    height=600
)

fig.show()
```

#### Creating Animations

```python
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    # Update plot with frame data
    ax.plot(x[frame], y[frame], z[frame])
    return ax,

ani = FuncAnimation(fig, update, frames=num_frames,
                   interval=50, blit=False)
plt.show()
```

### Debugging Common Issues

1. **Import Errors**:
   - Ensure all required libraries are installed
   - Check for typos in import statements
   - Verify library aliases match conventions

2. **Visualization Not Showing**:
   - Ensure `plt.show()` or `fig.show()` is called
   - Check if running in appropriate environment (Jupyter, script, etc.)

3. **Dimension Mismatches**:
   - Verify `meshgrid` usage for 3D plots
   - Check array shapes with `.shape` attribute
   - Ensure X, Y, Z have compatible dimensions

4. **Mathematical Errors**:
   - Validate calculations with `sympy` for symbolic verification
   - Check for division by zero
   - Handle domain restrictions (sqrt of negative, log of zero, etc.)

## Domain-Specific Knowledge

### Electrical Engineering

**Common Variables**:
- `V` - Voltage (Volts)
- `I` - Current (Amperes)
- `R` - Resistance (Ohms)
- `P` - Power (Watts)
- `EMF` - Electromotive Force
- `omega` - Angular frequency

**Key Formulas**:
- Ohm's Law: `V = I * R`
- Power: `P = V * I = I^2 * R = V^2 / R`
- AC Voltage: `V = V_max * sin(omega * t)`

### Physics & Mechanics

**Common Variables**:
- `theta` - Angle (radians)
- `omega` - Angular velocity
- `alpha` - Angular acceleration
- `F` - Force
- `m` - Mass
- `v` - Velocity

### Mathematics

**Trigonometry**:
- Common functions: `sin`, `cos`, `tan`, `sec`, `csc`, `cot`
- Identities frequently visualized
- Unit circle relationships

**Calculus**:
- Derivatives and integrals using `sympy`
- Taylor series expansions
- Integration visualizations

**Linear Algebra**:
- Matrix operations
- Transformations
- Eigenvalues/eigenvectors

## Testing & Validation

### Before Committing Code

1. **Run the script**: Ensure it executes without errors
2. **Check visualization**: Verify the plot displays correctly
3. **Validate mathematics**: Confirm calculations are accurate
4. **Review naming**: Ensure filename follows conventions
5. **Check imports**: Verify all required libraries are imported

### Quality Checklist

- [ ] Code runs without errors
- [ ] Visualization displays correctly
- [ ] Axes are properly labeled
- [ ] Title is descriptive
- [ ] Mathematical calculations are correct
- [ ] File name follows conventions
- [ ] Imports follow standard patterns
- [ ] Code is readable and commented where necessary

## Performance Considerations

1. **Large Datasets**:
   - Use appropriate point density for 3D meshes
   - Consider downsampling for interactive plots
   - Use `dtype=float32` for large arrays if precision allows

2. **Animations**:
   - Limit frame count for smooth playback
   - Adjust `interval` parameter for timing
   - Use `blit=True` when possible for matplotlib

3. **Interactive Plots**:
   - Plotly handles large datasets better than matplotlib for 3D
   - Consider using `scattergl` for large scatter plots
   - Limit marker count for responsive interaction

## Environment Setup

### Required Libraries

While there's no `requirements.txt`, the repository requires:

```
numpy
matplotlib
pandas
plotly
sympy
networkx
torch (for some scripts)
scikit-learn (for some scripts)
scipy
ipywidgets (for interactive notebooks)
```

### Installation

```bash
pip install numpy matplotlib pandas plotly sympy networkx torch scikit-learn scipy ipywidgets
```

## Best Practices for AI Assistants

1. **Understanding Context**:
   - This is a **visualization-focused** repository
   - Mathematical accuracy is critical
   - Visual clarity is paramount
   - Educational value is important

2. **When Creating New Files**:
   - Ask about the specific mathematical/physical concept
   - Determine appropriate dimensionality (2D vs 3D)
   - Choose suitable visualization library (matplotlib vs plotly)
   - Follow naming conventions strictly

3. **When Modifying Existing Files**:
   - Read the entire file first
   - Understand the mathematical concept being visualized
   - Preserve the original intent and structure
   - Improve clarity, not complexity

4. **Code Generation Principles**:
   - Prioritize readability over cleverness
   - Include descriptive comments for formulas
   - Use standard library aliases
   - Follow established patterns in similar files

5. **Avoiding Common Mistakes**:
   - Don't create subdirectories
   - Don't rename files without understanding impact
   - Don't add unnecessary dependencies
   - Don't over-complicate simple visualizations
   - Don't skip labels and titles

6. **Git Operations**:
   - Always commit to the designated feature branch
   - Use descriptive commit messages
   - Include file type in commit message (e.g., "Add: 3D visualization...")
   - Push with `-u origin <branch-name>` format
   - Retry on network failures with exponential backoff

## Additional Resources

### Mathematical Notation
- Use LaTeX-style notation in comments when helpful
- Example: `# Calculate: ∫sin(x)dx = -cos(x) + C`

### Visualization Best Practices
- Use colorblind-friendly colormaps when possible
- Ensure sufficient contrast for readability
- Add grid lines for reference when helpful
- Include legends for multi-series plots

### Common Pitfalls
1. Forgetting `plt.show()` at the end
2. Using wrong axis for 3D projections
3. Mismatched array dimensions in mesh grids
4. Missing imports for specific features
5. Incorrect mathematical formulas

## Repository Statistics

- **Total Files**: ~1000 Python scripts
- **Primary Focus**: Mathematical and scientific visualization
- **Visualization Types**: 2D plots, 3D plots, animations, interactive plots
- **Domains Covered**: Mathematics, physics, electrical engineering, statistics
- **Main Libraries**: NumPy, Matplotlib, Plotly, SymPy

---

**Last Updated**: 2025-11-24
**Repository**: STLNFTART/Data_Visualization
**Branch**: claude/claude-md-micf511gngvbu23v-01CXGFSWju7DKwSYYvEwyCuN

---

*This document is designed to help AI assistants understand and work effectively with this codebase. When in doubt, refer to existing files for patterns and conventions.*
