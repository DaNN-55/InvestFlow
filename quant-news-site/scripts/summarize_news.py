"""Manual summarize script for MVP stored news items."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.jobs import run_summarize_job  # noqa: E402


if __name__ == "__main__":
    changed = run_summarize_job()
    print(f"Summarize job done. updated={changed}")
