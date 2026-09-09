import argparse

from . import config
from .monitor import watch


def main():
    parser = argparse.ArgumentParser(
        prog="drive-defender",
        description="Real-time file monitor that flags and optionally quarantines suspicious files on a drive.",
    )
    parser.add_argument(
        "--drive", default=config.DEFAULT_DRIVE,
        help=f"Drive or folder path to watch (default: {config.DEFAULT_DRIVE})",
    )
    parser.add_argument(
        "--quarantine", action="store_true",
        help="Automatically move suspicious files to the quarantine folder",
    )
    parser.add_argument(
        "--no-recursive", action="store_true",
        help="Only watch the top-level directory, not subfolders",
    )
    args = parser.parse_args()

    watch(drive=args.drive, auto_quarantine=args.quarantine, recursive=not args.no_recursive)


if __name__ == "__main__":
    main()
