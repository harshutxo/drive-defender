import argparse
import sys

from . import config
from .monitor import watch
from .updater import update_signatures


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
    parser.add_argument(
        "--no-auto-update", action="store_true",
        help="Don't check GitHub for updated suspicious-file signatures",
    )
    parser.add_argument(
        "--update-signatures", action="store_true",
        help="Force-fetch the latest signatures from GitHub now and exit",
    )
    args = parser.parse_args()

    if args.update_signatures:
        updated = update_signatures(force=True)
        sys.exit(0 if updated else 1)

    watch(
        drive=args.drive,
        auto_quarantine=args.quarantine,
        recursive=not args.no_recursive,
        auto_update=not args.no_auto_update,
    )


if __name__ == "__main__":
    main()
