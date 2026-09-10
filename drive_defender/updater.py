import json
import time
import urllib.error
import urllib.request
from typing import NamedTuple

from . import config
from .logger import get_logger

logger = get_logger()


class Signatures(NamedTuple):
    extensions: set[str]
    filenames: set[str]


def _validate(data: dict) -> Signatures:
    extensions = data["extensions"]
    filenames = data["filenames"]
    if not isinstance(extensions, list) or not all(isinstance(e, str) for e in extensions):
        raise ValueError("extensions must be a list of strings")
    if not isinstance(filenames, list) or not all(isinstance(f, str) for f in filenames):
        raise ValueError("filenames must be a list of strings")
    return Signatures(
        extensions={e.lower() for e in extensions},
        filenames={f.lower() for f in filenames},
    )


def _read_local(path) -> Signatures | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return _validate(json.load(f))
    except (OSError, ValueError, KeyError):
        return None


def load_signatures() -> Signatures:
    """Load signatures from the auto-update cache, falling back to the bundled defaults."""
    cached = _read_local(config.SIGNATURES_CACHE)
    if cached is not None:
        return cached

    bundled = _read_local(config.BUNDLED_SIGNATURES)
    if bundled is not None:
        return bundled

    raise RuntimeError("No signature data available (cache and bundled defaults both missing/invalid)")


def _cache_age_hours() -> float:
    try:
        mtime = config.SIGNATURES_CACHE.stat().st_mtime
    except OSError:
        return float("inf")
    return (time.time() - mtime) / 3600


def update_signatures(force: bool = False) -> bool:
    """Fetch the latest signatures from GitHub and refresh the local cache.

    Returns True if the cache was updated, False if skipped or the fetch failed
    (in which case the previous cache/bundled defaults remain in effect).
    """
    if not force and _cache_age_hours() < config.SIGNATURE_UPDATE_INTERVAL_HOURS:
        logger.info("Signature cache is fresh, skipping auto-update")
        return False

    try:
        with urllib.request.urlopen(config.SIGNATURE_REMOTE_URL, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        _validate(data)  # raises if malformed
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        logger.warning("Signature auto-update failed (%s); keeping existing rules", exc)
        return False

    config.APP_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.SIGNATURES_CACHE, "w", encoding="utf-8") as f:
        f.write(raw)

    logger.info("Signatures updated from %s", config.SIGNATURE_REMOTE_URL)
    return True
