"""Manual fetch script for MVP RSS sources."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.jobs import run_fetch_job  # noqa: E402


if __name__ == "__main__":
    added, updated, errors = run_fetch_job()
    print(f"Fetch job done. added={added}, updated={updated}, errors={len(errors)}")
    for err in errors:
        print(f"  - {err}")

