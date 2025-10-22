# EPP Screening Model - External Usage Example

This example project demonstrates how to use the **EPP Screening Model** package as an external dependency in your own Python projects.

## Overview

This example shows how an external team or scientist can:
- Install the EPP Screening Model package from GitHub
- Use the goal seek API with custom ACCU volumes
- Run batch sensitivity analyses
- Execute full model calculations programmatically

## Prerequisites

- **Python 3.12+**
- **UV package manager** (recommended) or pip
- **GitHub authentication** (one of):
  - GitHub Personal Access Token (PAT)
  - SSH keys configured with GitHub
  - GitHub CLI (gh) authenticated

## Installation

### Option 1: Using GitHub Personal Access Token (Most Common)

1. **Create a GitHub Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Copy the token (you'll only see it once!)

2. **Set up authentication**:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your GitHub token
   # GITHUB_TOKEN=ghp_your_token_here
   ```

3. **Install the EPP package**:
   ```bash
   # Using UV (recommended) - specify v1.1.0 or later
   uv add "git+https://${GITHUB_TOKEN}@github.com/MullionGroup/epp_screening_model_v3.git@v1.1.0"

   # Or using pip
   pip install "git+https://${GITHUB_TOKEN}@github.com/MullionGroup/epp_screening_model_v3.git@v1.1.0"
   ```

   **Important**: Version 1.1.0 or later is required for the Jupyter helper functions.

### Option 2: Using SSH Keys (For Developers)

If you have SSH keys configured with GitHub:

```bash
# Using UV - specify v1.1.0 or later
uv add "git+ssh://git@github.com/MullionGroup/epp_screening_model_v3.git@v1.1.0"

# Or using pip
pip install "git+ssh://git@github.com/MullionGroup/epp_screening_model_v3.git@v1.1.0"
```

### Option 3: Using GitHub CLI (Easiest for macOS)

If you have GitHub CLI installed and authenticated:

```bash
# Authenticate first (uses 1Password/Keychain)
gh auth login

# Install package - specify v1.1.0 or later
uv add "git+https://github.com/MullionGroup/epp_screening_model_v3.git@v1.1.0"
```

## Quick Start

### 1. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Up Configuration

Copy the base configuration from the EPP package or create your own:

```bash
# Create a config directory
mkdir -p config

# You'll need a config.toml file - see examples/01_basic_goal_seek.py
```

### 3. Run Examples

#### Option A: Interactive Jupyter Notebook (Recommended)

```bash
# Install notebook dependencies
uv sync --extra notebook

# Launch Jupyter notebook (from project root or examples directory)
uv run jupyter notebook examples/EPP_Examples.ipynb
```

The notebook:
- Automatically adjusts the working directory to find config files
- Provides step-by-step explanations
- Includes interactive code cells
- Generates visualizations and charts
- Contains all examples in one place

#### Option B: Python Scripts

```bash
# Example 1: Basic goal seek
uv run python examples/01_basic_goal_seek.py

# Example 2: Custom ACCU volumes
uv run python examples/02_custom_accu_volumes.py

# Example 3: Batch sensitivity analysis
uv run python examples/03_batch_analysis.py

# Example 4: Full model execution
uv run python examples/04_full_model_run.py
```

## Example Scripts

### Jupyter Notebook (Recommended for Learning)

**[EPP_Examples.ipynb](examples/EPP_Examples.ipynb)** - Interactive notebook covering all examples:
- Basic goal seek with presets
- Custom ACCU volumes
- Batch sensitivity analysis
- Visualizations and exports
- Step-by-step explanations

To use the notebook:
```bash
# Install Jupyter dependencies
uv sync --extra notebook

# Start Jupyter (from project root or examples directory)
uv run jupyter notebook examples/EPP_Examples.ipynb

# The notebook automatically adjusts the working directory
```

### Python Scripts

### 01_basic_goal_seek.py
Demonstrates basic goal seek using presets:
- Find LVR for target debt ratio
- Find property price for target IRR
- Access financial metrics from results

### 02_custom_accu_volumes.py
Shows how to use custom ACCU volumes:
- Pass ACCU volumes as Python lists
- No TOML files required
- Combine with parameter overrides

### 03_batch_analysis.py
Performs sensitivity analysis:
- Compare multiple ACCU scenarios
- Generate summary DataFrame
- Export results to CSV

### 04_full_model_run.py
Demonstrates full model execution:
- Run complete 9-sheet model
- Access individual sheet results
- Export to multiple formats

## Project Structure

```
epp-example-external-usage/
├── README.md                    # This file
├── pyproject.toml              # UV project configuration
├── .env.example                # GitHub token template
├── .gitignore                  # Git ignore rules
├── examples/
│   ├── EPP_Examples.ipynb      # Interactive Jupyter notebook (recommended)
│   ├── 01_basic_goal_seek.py
│   ├── 02_custom_accu_volumes.py
│   ├── 03_batch_analysis.py
│   └── 04_full_model_run.py
├── config/
│   └── config.toml             # Model configuration
├── data/
│   └── scenarios/              # Custom scenario files
└── results/                    # Output directory
```

## Configuration

The EPP Screening Model requires a `config.toml` file with model parameters. See the main EPP repository for configuration templates and examples.

Key configuration sections:
- **[static]** - Static model parameters (property price, hectares, etc.)
- **[csv_data_paths]** - Paths to CSV data files
- **[scenario]** - Optional scenario overrides (ACCU volumes, etc.)

## API Documentation

### Goal Seek with Presets

```python
from epp_screening_model_v3.models.goal_seek import GoalSeekSolver, get_preset

solver = GoalSeekSolver('config/config.toml')
preset = get_preset('debt-ratio-60')

result = solver.solve(
    input_cell=preset.input_cell,
    target_cell=preset.target_cell,
    target_value=preset.target_value,
    bounds=(preset.min_value, preset.max_value)
)

print(f"Optimal LVR: {result.solution:.2%}")
print(f"Levered Return: {result.levered_return:.2%}")
```

### Goal Seek with Custom ACCU Volumes (v1.1.0+)

**Recommended Method** - Using Jupyter helpers:

```python
from epp_screening_model_v3.notebooks.epp_jupyter_helpers import goal_seek_with_accu_volumes

# Pass ACCU volumes as Python list - no TOML files needed!
result = goal_seek_with_accu_volumes(
    preset_name='debt-ratio-60',
    accu_volumes=[0.0, 6750.0, 24605.5, ..., 0.0, 0.0],  # 27 values
    config_path='config/config.toml'
)

print(f"Optimal LVR: {result.solution:.2%}")
print(f"Levered Return: {result.levered_return:.2%}")
```

### Batch Sensitivity Analysis (v1.1.0+)

```python
from epp_screening_model_v3.notebooks.epp_jupyter_helpers import batch_goal_seek_analysis

scenarios = {
    'Conservative': [0.0, 4500.0, ...],  # 27 values
    'Baseline': [0.0, 6000.0, ...],      # 27 values
    'Aggressive': [0.0, 6750.0, ...],    # 27 values
}

df = batch_goal_seek_analysis(
    preset_name='debt-ratio-60',
    accu_scenarios=scenarios,
    config_path='config/config.toml'
)

print(df[['scenario', 'lvr', 'unlevered_return', 'levered_return']])
```

### Full Model Execution

```python
from epp_screening_model_v3.models import ACCUModel

model = ACCUModel('config/config.toml')
results = model.calculate_full_model()

print(f"Unlevered IRR: {results.unlevered_irr:.2%}")
print(f"Levered IRR: {results.levered_irr:.2%}")

# Access individual sheets
returns_data = results.get_sheet_result('Returns_Prj')
```

## Available Presets

**Debt Ratios** (adjust LVR):
- `debt-ratio-50` - Target 50% debt-to-capex
- `debt-ratio-60` - Target 60% debt-to-capex
- `debt-ratio-70` - Target 70% debt-to-capex

**Levered Returns** (adjust Property Price):
- `levered-return-12` - Target 12% levered IRR
- `levered-return-15` - Target 15% levered IRR
- `levered-return-18` - Target 18% levered IRR
- `levered-return-20` - Target 20% levered IRR

**Unlevered Returns** (adjust Property Price):
- `unlevered-return-10` - Target 10% unlevered IRR
- `unlevered-return-12` - Target 12% unlevered IRR
- `unlevered-return-15` - Target 15% unlevered IRR

## Troubleshooting

### Authentication Issues

**Problem**: `fatal: could not read Username for 'https://github.com'`

**Solution**: Make sure you've set up authentication using one of the three methods above.

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'epp_screening_model_v3'`

**Solution**:
```bash
# Verify installation
uv pip list | grep epp-screening-model

# Reinstall if needed
uv add git+https://github.com/MullionGroup/epp_screening_model_v3.git --force-reinstall
```

### Import Errors

**Problem**: Package imports not working

**Solution**: Make sure you're using the correct import paths:
```python
# Correct
from epp_screening_model_v3.models import ACCUModel
from epp_screening_model_v3.models.goal_seek import GoalSeekSolver

# Incorrect
from epp_screening_model import ACCUModel  # Wrong package name
```

## Support

For issues, questions, or feature requests:
- Main Repository: https://github.com/MullionGroup/epp_screening_model_v3
- Documentation: See `docs/` in the main repository
- Issues: https://github.com/MullionGroup/epp_screening_model_v3/issues

## License

This example project is for demonstration purposes. The EPP Screening Model package is subject to its own license terms.

## Version Compatibility

This example project requires:
- **EPP Screening Model v1.1.0 or later** (for Jupyter helper functions)
- **Python 3.12+**
- **UV 0.5.0+** (recommended) or pip

**Version History**:
- v1.0.6: Package build was broken (skip this version)
- v1.0.7: Fixed package imports
- v1.0.8: Added scenario class exports
- v1.0.9: Includes Jupyter helpers for convenient API
- v1.1.0: **Recommended** - Latest stable release

Last updated: 2025-10-21
