#!/usr/bin/env python3
"""
Forward Deployment Job Scraper (India - Freshers & Entry Level)
----------------------------------------------------------------
Scrapes websites and career platforms for Forward Deployed Engineer (FDE / FDSE)
job openings in India, specifically classified and filtered for freshers and early-career engineers.

Usage:
    python scrape_jobs.py
    python scrape_jobs.py --location Bengaluru --pages 3
    python scrape_jobs.py --sources ats,linkedin --fetch-details
    python scrape_jobs.py --all-experience
"""

import sys
import os
import argparse
import logging
from fde_job_scraper.aggregator import JobAggregator
from fde_job_scraper.exporter import JobExporter
from fde_job_scraper.config import DEFAULT_KEYWORDS, FRESHER_KEYWORDS

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def setup_logger(verbose: bool = False):
    """Sets up formatted terminal logging."""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(level=level, format=format_str, datefmt="%H:%M:%S")

def print_banner():
    """Prints decorative banner."""
    print("=" * 75)
    print("  [+] FORWARD DEPLOYMENT JOB SCRAPER - INDIA (FRESHERS & ENTRY LEVEL)")
    print("=" * 75)

def print_summary_table(postings, max_display=15):
    """Prints a clean tabular summary to the terminal."""
    if not postings:
        print("\n[!] No matching job openings found.")
        return

    print(f"\nFound {len(postings)} Matching Openings:\n")
    header = f"{'COMPANY':<18} | {'ROLE TITLE':<35} | {'LOCATION':<22} | {'EXPERIENCE':<18}"
    print(header)
    print("-" * len(header))

    for p in postings[:max_display]:
        comp = p.company[:16]
        title = p.title[:33]
        loc = p.location[:20]
        exp = p.experience_level[:17]
        print(f"{comp:<18} | {title:<35} | {loc:<22} | {exp:<18}")

    if len(postings) > max_display:
        print(f"\n... and {len(postings) - max_display} more postings (see exported files).")

def main():
    parser = argparse.ArgumentParser(
        description="Scrape websites for Forward Deployment engineering job openings in India for freshers."
    )
    parser.add_argument(
        "--location",
        default="India",
        help="Target location in India (e.g. 'India', 'Bengaluru', 'Hyderabad', 'Pune', 'Noida', 'Mumbai')"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=None,
        help="Custom search keywords (e.g. --keywords 'forward deployed engineer' 'fde AI')"
    )
    parser.add_argument(
        "--all-experience",
        action="store_true",
        help="Include all experience levels (disables fresher-only filter)"
    )
    parser.add_argument(
        "--sources",
        default="all",
        help="Sources to scrape: 'all', 'linkedin', 'ats', 'remote' (comma-separated)"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=2,
        help="Max search pages per keyword for LinkedIn (default: 2)"
    )
    parser.add_argument(
        "--fetch-details",
        action="store_true",
        help="Fetch full job descriptions for deep experience parsing (slower, respectful delays)"
    )
    parser.add_argument(
        "--output-dir",
        default="./job_results",
        help="Directory to save scraped output (default: ./job_results)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed debug logs"
    )

    args = parser.parse_args()
    setup_logger(args.verbose)
    print_banner()

    fresher_only = not args.all_experience
    sources = [s.strip() for s in args.sources.split(",")]

    print(f"[*] Target Location : {args.location}")
    print(f"[*] Fresher Filter  : {'ENABLED (Freshers / Entry Level only)' if fresher_only else 'DISABLED (All Experience)'}")
    print(f"[*] Sources Active  : {', '.join(sources)}")
    print(f"[*] Output Dir      : {args.output_dir}\n")

    # Run scraping pipeline
    aggregator = JobAggregator(sources=sources)
    postings = aggregator.run(
        keywords=args.keywords,
        location=args.location,
        fresher_only=fresher_only,
        max_pages=args.pages,
        fetch_details=args.fetch_details
    )

    # Print summary to console
    print_summary_table(postings)

    # Export to files
    if postings:
        exporter = JobExporter(output_dir=args.output_dir)
        files = exporter.export_all(postings)
        print("\n" + "=" * 75)
        print("  [OK] EXPORT COMPLETE")
        print("=" * 75)
        print(f"  * JSON Report     : {files['json']}")
        print(f"  * CSV Spreadsheet : {files['csv']}")
        print(f"  * Markdown Digest : {files['markdown']}")
        print("=" * 75 + "\n")
    else:
        print("\n[!] No matching postings to export.")

if __name__ == "__main__":
    main()
