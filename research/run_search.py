#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
run_search.py

Script to run academic paper searches using findpapers for PT-BR voice/speech corpus research.
Configured for:
1. Medical & Telehealth PT-BR speech datasets.
2. Meetings & Videoconference spontaneous speech in PT-BR.
3. Conversational spontaneous speech in PT-BR (contingency).
"""

import os
import argparse
import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv

import findpapers
from findpapers import Engine
from findpapers.core.search_result import SearchResult

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("run_search")

# Define the search queries
QUERIES = {
    1: {
        "name": "medical_telehealth_pt",
        "description": "Para Áudios Médicos e de Teleatendimento em PT-BR (Foco Principal)",
        "query": (
            '("medical speech" OR "clinical audio" OR "doctor-patient conversation" OR '
            '"telemedicina" OR "teleatendimento") AND ("Portuguese" OR "PT-BR") AND ("dataset" OR "corpus")'
        )
    },
    2: {
        "name": "meeting_videoconference_pt",
        "description": "Para Áudios Extraídos de Plataformas de Meetings / Videoconferências (O 'Plus')",
        "query": (
            '("meeting recordings" OR "video conference" OR "teleconference" OR "Zoom" OR "telehealth") '
            'AND ("spontaneous speech" OR "conversational audio") AND ("Portuguese" OR "PT-BR")'
        )
    },
    3: {
        "name": "conversational_spontaneous_pt",
        "description": "Para Fala Conversacional e Espontânea em PT-BR (Plano de Contingência)",
        "query": (
            '("conversational speech" OR "spontaneous speech" OR "fala espontânea" OR "fala conversacional" '
            'OR "dialogue") AND ("hesitations" OR "non-lexical" OR "overlapping") AND ("Portuguese" OR "PT-BR")'
        )
    }
}


def parse_date(date_str: str) -> datetime.date | None:
    if not date_str:
        return None
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Must be YYYY-MM-DD.")


def load_environment():
    """Load env files from current directory, parent directory or research directory."""
    # Try local run folder
    load_dotenv()
    # Try research/ folder if running from project root
    load_dotenv(Path(__file__).parent / ".env")
    # Try project root if running from research folder
    load_dotenv(Path(__file__).parent.parent / ".env")


def merge_results(results: list[SearchResult], combined_query_desc: str) -> SearchResult:
    """Merge multiple SearchResult objects, performing field-aware paper deduplication."""
    logger.info("Merging and deduplicating results...")
    merged_papers = []
    seen_papers = {}  # key -> Paper
    
    for r in results:
        for p in r.papers:
            key = p._identity_key()
            if not key:
                # If no identity key (no DOI, no Title), keep it just in case
                merged_papers.append(p)
                continue
            if key in seen_papers:
                # Merge fields (citations, found_in databases, authors, etc.)
                seen_papers[key].merge(p)
            else:
                seen_papers[key] = p
                merged_papers.append(p)
                
    logger.info(f"Deduplication completed. Total unique papers: {len(merged_papers)}")
    
    # Instantiate a unified search result
    merged_result = SearchResult(
        query=combined_query_desc,
        papers=merged_papers,
        processed_at=datetime.datetime.now(datetime.UTC),
    )
    return merged_result


def main():
    parser = argparse.ArgumentParser(
        description="Search for academic papers across databases using findpapers.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-q", "--queries",
        nargs="+",
        type=int,
        choices=[1, 2, 3],
        default=[1, 2, 3],
        help="Indices of the queries to run (default: 1 2 3)"
    )
    parser.add_argument(
        "-s", "--since",
        type=parse_date,
        default="2016-01-01",
        help="Start publication date (YYYY-MM-DD, default: 2016-01-01)"
    )
    parser.add_argument(
        "-u", "--until",
        type=parse_date,
        default=None,
        help="End publication date (YYYY-MM-DD, default: None/Today)"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=None,
        help="Max papers retrieved per database (default: no limit)"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Number of concurrent worker threads (default: 4)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=str(Path(__file__).parent / "results"),
        help="Directory to save search results (default: research/results)"
    )
    parser.add_argument(
        "-d", "--download-dir",
        type=str,
        default=None,
        help="If set, downloads PDFs to this directory (default: None)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debugging logs"
    )

    args = parser.parse_args()

    # Configure logs verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("findpapers").setLevel(logging.DEBUG)

    load_environment()

    # Check API key configuration for warning
    email = os.environ.get("FINDPAPERS_EMAIL")
    if not email:
        logger.warning(
            "FINDPAPERS_EMAIL is not set. You are highly likely to be rate-limited by CrossRef and OpenAlex. "
            "Consider setting it in a .env file."
        )

    # Initialize Engine (it automatically reads from environment variables)
    logger.info("Initializing findpapers Engine...")
    engine = Engine()

    # Create output directories
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = []
    
    for q_idx in args.queries:
        q_info = QUERIES[q_idx]
        logger.info("=" * 60)
        logger.info(f"Running Query {q_idx}: {q_info['description']}")
        logger.info(f"Query String: {q_info['query']}")
        logger.info("=" * 60)
        
        try:
            # Execute search
            result = engine.search(
                query=q_info["query"],
                since=args.since,
                until=args.until,
                max_papers_per_database=args.limit,
                num_workers=args.workers,
                verbose=args.verbose,
                show_progress=True
            )
            
            logger.info(f"Query {q_idx} finished. Found {len(result.papers)} papers.")
            
            # Save individual results
            json_file = output_path / f"query_{q_idx}_{q_info['name']}.json"
            bib_file = output_path / f"query_{q_idx}_{q_info['name']}.bib"
            
            findpapers.save_to_json(result, str(json_file))
            findpapers.save_to_bibtex(result.papers, str(bib_file))
            logger.info(f"Results saved to:\n  - {json_file}\n  - {bib_file}")
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"Failed to execute Query {q_idx}: {e}", exc_info=True)

    # Merge results if multiple queries were run
    if len(results) > 1:
        logger.info("=" * 60)
        logger.info("Merging multiple query results...")
        logger.info("=" * 60)
        
        combined_desc = "Combined PT-BR Audio Dataset Search (Queries " + ", ".join(map(str, args.queries)) + ")"
        merged_result = merge_results(results, combined_desc)
        
        merged_json = output_path / "combined_results.json"
        merged_bib = output_path / "combined_results.bib"
        
        findpapers.save_to_json(merged_result, str(merged_json))
        findpapers.save_to_bibtex(merged_result.papers, str(merged_bib))
        logger.info(f"Merged results saved to:\n  - {merged_json}\n  - {merged_bib}")
        
        final_papers_list = merged_result.papers
    elif len(results) == 1:
        final_papers_list = results[0].papers
    else:
        logger.error("No queries executed successfully.")
        return

    # Optional PDF downloading
    if args.download_dir and final_papers_list:
        logger.info("=" * 60)
        logger.info(f"Downloading PDFs to {args.download_dir}...")
        logger.info("=" * 60)
        download_path = Path(args.download_dir)
        download_path.mkdir(parents=True, exist_ok=True)
        
        try:
            engine.download(final_papers_list, str(download_path))
            logger.info("PDF downloads completed.")
        except Exception as e:
            logger.error(f"Error downloading PDFs: {e}", exc_info=True)


if __name__ == "__main__":
    main()
