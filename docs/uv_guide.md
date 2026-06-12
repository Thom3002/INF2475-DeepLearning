# uv — Environment Management Guide

> Quick reference for managing the project environment with `uv`.
> Official docs: https://docs.astral.sh/uv/

---

## What is `uv`?

`uv` is an extremely fast Python package and project manager written in Rust. It replaces `pip`, `pip-tools`, `venv`, and partially `conda` in a single tool.

---

## Installation

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

---

## Core Concepts

| Concept | `uv` equivalent | `conda` equivalent |
|---|---|---|
| Create environment | `uv sync` (automatic) | `conda create -n myenv` |
| Activate environment | `source .venv/bin/activate` | `conda activate myenv` |
| Install dependencies | `uv sync` | `conda install` / `pip install` |
| Add a new package | `uv add <package>` | `pip install` + update yml |
| Remove a package | `uv remove <package>` | `pip uninstall` + update yml |
| Lock file | `uv.lock` (auto-generated) | `environment.yml` (manual) |
| Run without activating | `uv run <command>` | N/A |

---

## Daily Workflow

### First-time setup (clone → ready to work)
```bash
# Install all deps (production + dev) and create .venv automatically
uv sync --extra dev

# Activate the environment
source .venv/bin/activate
```

### Adding a new package
```bash
# Production dependency
uv add transformers

# Development-only dependency (not installed in production)
uv add --dev pytest

# With version constraint
uv add "torch>=2.2.0"
```

### Removing a package
```bash
uv remove <package-name>
```

### Running commands without activating the venv
```bash
# Run a script
uv run python scripts/train.py

# Run jupyter
uv run jupyter lab

# Run the API
uv run uvicorn api.main:app --reload
```

### Updating all packages to latest compatible versions
```bash
uv lock --upgrade
uv sync
```

### Installing a specific Python version
```bash
# uv manages Python versions automatically
uv python install 3.11
uv python pin 3.11  # pins this project to Python 3.11
```

---

## Key Files

| File | Purpose | Commit to Git? |
|---|---|---|
| `pyproject.toml` | Declares project deps and metadata | ✅ Yes |
| `uv.lock` | Exact pinned versions (reproducibility) | ✅ Yes |
| `.venv/` | The actual virtual environment | ❌ No (gitignored) |

> **Important**: Always commit `uv.lock`. It ensures everyone (and every machine) gets exactly the same package versions.

---

## Reproducing the Environment on a New Machine

```bash
# Clone the repo
git clone <repo-url>
cd INF2475-DeepLearning

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recreate exact environment from lock file
uv sync --extra dev

# Done!
source .venv/bin/activate
```

---

## Useful Commands

```bash
# List installed packages
uv pip list

# Show dependency tree
uv tree

# Check for outdated packages
uv lock --upgrade --dry-run

# Export to requirements.txt (for compatibility)
uv export --format requirements-txt > requirements.txt

# Show environment info
uv python list
```

---

## Tips for ML Projects

1. **PyTorch with CUDA**: If you need a specific CUDA version of PyTorch, install it manually after `uv sync`:
   ```bash
   uv add "torch==2.2.0+cu121" --index-url https://download.pytorch.org/whl/cu121
   ```

2. **Jupyter kernel**: Register the venv as a Jupyter kernel:
   ```bash
   uv run python -m ipykernel install --user --name consultaai --display-name "ConsultaAI (Python 3.11)"
   ```

3. **VS Code integration**: Open the project in VS Code and select the interpreter at `.venv/bin/python`.
