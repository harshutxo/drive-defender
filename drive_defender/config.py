from pathlib import Path

# Extensions treated as suspicious when they appear as new or modified files.
SUSPICIOUS_EXTENSIONS = {
    ".exe", ".scr", ".bat", ".cmd", ".vbs", ".vbe", ".js", ".jse",
    ".ps1", ".psm1", ".msi", ".dll", ".lnk", ".hta", ".jar",
}

# Filenames that are classic autorun/malware droppers.
SUSPICIOUS_FILENAMES = {"autorun.inf", "desktop.ini.exe"}

DEFAULT_DRIVE = "D:\\"
APP_DIR = Path.home() / ".drive_defender"
QUARANTINE_DIR = APP_DIR / "quarantine"
LOG_FILE = APP_DIR / "drive_defender.log"
