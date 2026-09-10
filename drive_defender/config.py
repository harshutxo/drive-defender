from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
BUNDLED_SIGNATURES = PACKAGE_DIR / "data" / "signatures.json"

DEFAULT_DRIVE = "D:\\"
APP_DIR = Path.home() / ".drive_defender"
QUARANTINE_DIR = APP_DIR / "quarantine"
LOG_FILE = APP_DIR / "drive_defender.log"

# Auto-updated signatures (extensions/filenames) are cached here.
SIGNATURES_CACHE = APP_DIR / "signatures.json"

# User-maintained additions, merged on top of the auto-updated signatures.
# Same schema as signatures.json: {"extensions": [...], "filenames": [...]}
CUSTOM_SIGNATURES = APP_DIR / "custom_signatures.json"
SIGNATURE_REMOTE_URL = (
    "https://raw.githubusercontent.com/harshutxo/drive-defender/main/"
    "drive_defender/data/signatures.json"
)
SIGNATURE_UPDATE_INTERVAL_HOURS = 24
