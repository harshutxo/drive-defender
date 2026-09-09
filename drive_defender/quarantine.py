import shutil
import time
from pathlib import Path

from . import config


def quarantine_file(path: Path) -> Path | None:
    """Move a suspicious file into the quarantine folder. Returns the new path, or None on failure."""
    config.QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        return None

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    dest = config.QUARANTINE_DIR / f"{timestamp}_{path.name}"

    try:
        shutil.move(str(path), str(dest))
        return dest
    except OSError:
        return None
