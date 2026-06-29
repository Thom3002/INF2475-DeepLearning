# ConsultaAI — SOAP Structuring for Medical Transcripts (SUS)

> **INF2475 — Introduction to Deep Learning | Master's Degree Project**


## Repository Structure

```
.
├── configs/            # Experiment configuration files (.yaml)
├── data/               # Datasets — NOT versioned (see .gitignore)
│   ├── input/
│   │   ├── raw/        # Original C-ORAL-ESQ dataset
│   │   └── processed/  # Preprocessed audio segments and metadata.csv
│   └── output/         # Evaluation results and predictions
├── models/             # Model weights/checkpoints — NOT versioned
├── notebooks/          # Exploratory and experimental notebooks
├── src/                # Core reusable Python modules (installable package)
│   ├── data/
│   ├── preprocessing/
│   ├── models/
│   ├── evaluation/
│   └── utils/
├── scripts/            # CLI entry points for pipeline stages
├── api/                # FastAPI inference & evaluation server
├── tests/              # Unit tests
└── docs/               # Project documentation
```

## Quickstart

### 1. Install `uv` (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Set up the environment
```bash
uv sync --extra dev
```

### 3. Activate the virtual environment
```bash
source .venv/bin/activate
```

### 4. Launch Jupyter
```bash
uv run jupyter lab
```

### 5. Run the API server
```bash
uv run uvicorn api.main:app --reload
```

See [`docs/uv_guide.md`](docs/uv_guide.md) for detailed environment management instructions.

## Academic Context

- **Course**: INF2475 — Introduction to Deep Learning
- **Institution**: PUC-Rio
- **Semester**: 2026.1
