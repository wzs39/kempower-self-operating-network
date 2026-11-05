"""
Cross-platform, zero-hardcode path resolver (Fixes GitHub Issue #2 Item D4).
Ensures all tests, simulation engines, and scripts run on any machine or OS.
"""

import os
from pathlib import Path


def get_repo_root() -> Path:
    """Returns the repository root directory dynamically relative to this file."""
    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    """
    Locates the directory containing the 45 official Kempower CSV files.
    Checks:
      1. KEMPOWER_DATA_DIR environment variable
      2. <repo_root>/kempower-challenge/kempower-challenge-data
      3. <repo_root>/kempower-challenge-data
      4. Parent directory ../kempower-challenge-data
    """
    env_dir = os.environ.get("KEMPOWER_DATA_DIR")
    if env_dir:
        p = Path(env_dir).expanduser().resolve()
        if p.is_dir():
            return p

    root = get_repo_root()
    candidates = [
        root / "kempower-challenge" / "kempower-challenge-data",
        root / "kempower-challenge-data",
        root.parent / "kempower-challenge-data",
        root.parent / "kempower-challenge" / "kempower-challenge-data",
    ]
    for cand in candidates:
        if cand.is_dir() and (cand / "sites.csv").is_file():
            return cand

    # Fallback to primary expected relative path
    return root / "kempower-challenge" / "kempower-challenge-data"


def resolve_csv_path(filename: str) -> Path:
    """Returns the full Path to a specific CSV in the official dataset."""
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"
    return get_data_dir() / filename
