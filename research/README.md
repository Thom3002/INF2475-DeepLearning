# PT-BR Audio Corpus and Dataset Academic Search

This folder contains the scripts, configurations, and results for the academic paper systematic search focused on finding speech datasets, clinical audios, spontaneous conversational speech, and meeting recordings in **Brazilian Portuguese (PT-BR)**.

These searches target building robust ASR (Automatic Speech Recognition) models under real teleconsultation acoustic conditions, leveraging existing literature and public databases.

## Objectives & Search Queries

We use three search strings defined to capture the main target, realistic acoustic proxies, and spontaneous speech contingency plans:

### 1. Medical & Telehealth PT-BR Speech (Main Goal)
*   **Search String**:
    ```sql
    ("medical speech" OR "clinical audio" OR "doctor-patient conversation" OR "telemedicina" OR "teleatendimento") AND ("Portuguese" OR "PT-BR") AND ("dataset" OR "corpus")
    ```
*   **Rationale**: Targets the ideal scenario of anonymized or simulated doctor-patient consultation recordings. Combines English terminology (for global metadata coverage) and Portuguese search criteria to maximize hits.

### 2. Meetings & Videoconference Recordings (Acoustic Proxy)
*   **Search String**:
    ```sql
    ("meeting recordings" OR "video conference" OR "teleconference" OR "Zoom" OR "telehealth") AND ("spontaneous speech" OR "conversational audio") AND ("Portuguese" OR "PT-BR")
    ```
*   **Rationale**: Telemedicine platforms expose speech to compression artifacts, variable microphonic quality, and network packet loss. Meeting recordings act as an excellent proxy for teaching models acoustic robustness under similar compression characteristics.

### 3. Spontaneous & Conversational PT-BR Speech (Contingency Plan)
*   **Search String**:
    ```sql
    ("conversational speech" OR "spontaneous speech" OR "fala espontânea" OR "fala conversacional" OR "dialogue") AND ("hesitations" OR "non-lexical" OR "overlapping") AND ("Portuguese" OR "PT-BR")
    ```
*   **Rationale**: Natural human speech contains overlapping voices, hesitations ("uh", "um"), and non-lexical sounds. ASR models trained on pristine reads fail in real dialogue; this contingency focuses on conversational datasets to handle spontaneous interruptions.

---

## Directory Structure

```
research/
├── .env.example        # Template for database API keys
├── README.md           # This documentation
├── requirements.txt    # Standalone pip dependency file
├── run_search.py       # Main Python CLI execution script
└── results/            # [Generated] Stores query and combined results (.json, .bib)
```

---

## Setup & Prerequisites

You can execute the search script using either your local `uv` environment or a standard python virtual environment.

### 1. Configure API Keys
Copy the template `.env.example` to `.env`:
```bash
cp research/.env.example research/.env
```
Open `research/.env` and configure your keys. 
*   **CrossRef & OpenAlex**: Setting `FINDPAPERS_EMAIL` is highly recommended to join the polite pool and prevent rate-limiting or blocking.
*   **Scopus, IEEE Xplore, Web of Science**: Require free developer API keys to search. Without them, the script will skip these databases.

### 2. Environment Setup

#### Option A: Using `uv` (Recommended)
Sync the workspace environment to install `findpapers` and `python-dotenv`:
```bash
uv sync
```
Verify the dependencies are synced:
```bash
uv run python -c "import findpapers; print(findpapers.__version__)"
```

#### Option B: Using standard Python (`pip`)
```bash
pip install -r research/requirements.txt
```

---

## Running the Search

The script `run_search.py` is a robust command-line tool with multiple customization options:

### 1. Test Search (Fast, limited results)
We recommend running a test with a cap of **10 papers per database** to verify the configuration and connection:
```bash
# Using uv
uv run python research/run_search.py --limit 10

# Using global python
python research/run_search.py --limit 10
```

### 2. Full Search
Run all queries since **2016** with parallel execution (4 workers) and no limit:
```bash
uv run python research/run_search.py --since 2016-01-01 --workers 4
```

### 3. Run a Specific Query
To only run the **Medical & Telehealth** search (Query 1):
```bash
uv run python research/run_search.py -q 1
```

### 4. Search and Download PDFs
Search and automatically download the resolved PDFs for matches:
```bash
uv run python research/run_search.py --limit 20 --download-dir research/pdfs
```

### CLI Arguments Reference

| Argument | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--queries` | `-q` | List | `1 2 3` | Select which queries to run (separated by space) |
| `--since` | `-s` | Date | `2016-01-01` | Start publication date (`YYYY-MM-DD`) |
| `--until` | `-u` | Date | `None` | End publication date (`YYYY-MM-DD`) |
| `--limit` | `-l` | Integer | `None` | Max papers retrieved per database (useful for testing) |
| `--workers` | `-w` | Integer | `4` | Number of parallel worker threads |
| `--output-dir` | `-o` | String | `research/results` | Folder to save search outputs |
| `--download-dir`| `-d` | String | `None` | If specified, downloads PDFs here |
| `--verbose` | | Flag | `False` | Enables detailed debug printing |

---

## Output Files

The script generates separate outputs for each individual query to allow isolated analysis, as well as a consolidated combined search result:

*   **Individual Query Results**:
    *   `query_1_medical_telehealth_pt.json` / `.bib`
    *   `query_2_meeting_videoconference_pt.json` / `.bib`
    *   `query_3_conversational_spontaneous_pt.json` / `.bib`
*   **Consolidated Search Result**:
    *   `combined_results.json` / `.bib` - Automatically merges duplicates using title/DOI-based deduplication and combines metadata fields.
