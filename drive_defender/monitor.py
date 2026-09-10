import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import config
from .logger import get_logger
from .quarantine import quarantine_file
from .updater import Signatures, load_signatures, update_signatures

logger = get_logger()

SIGNATURE_RECHECK_SECONDS = 3600


def is_suspicious(path: Path, signatures: Signatures) -> bool:
    if path.name.lower() in signatures.filenames:
        return True
    return path.suffix.lower() in signatures.extensions


class DriveDefenderHandler(FileSystemEventHandler):
    def __init__(self, signatures: Signatures, auto_quarantine: bool = False):
        super().__init__()
        self.signatures = signatures
        self.auto_quarantine = auto_quarantine

    def _handle(self, event_type: str, src_path: str):
        path = Path(src_path)
        if path.is_dir():
            return

        if is_suspicious(path, self.signatures):
            logger.warning("SUSPICIOUS %s: %s", event_type, path)
            if self.auto_quarantine:
                dest = quarantine_file(path)
                if dest:
                    logger.warning("QUARANTINED %s -> %s", path, dest)
                else:
                    logger.error("QUARANTINE FAILED for %s", path)
        else:
            logger.info("%s: %s", event_type, path)

    def on_created(self, event):
        if not event.is_directory:
            self._handle("CREATED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle("MODIFIED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._handle("MOVED", event.dest_path)


def watch(
    drive: str = config.DEFAULT_DRIVE,
    auto_quarantine: bool = False,
    recursive: bool = True,
    auto_update: bool = True,
):
    target = Path(drive)
    if not target.exists():
        logger.error("Drive/path does not exist: %s", target)
        return

    if auto_update:
        update_signatures()

    try:
        signatures = load_signatures()
    except RuntimeError as exc:
        logger.error("%s", exc)
        return

    handler = DriveDefenderHandler(signatures=signatures, auto_quarantine=auto_quarantine)
    observer = Observer()
    observer.schedule(handler, str(target), recursive=recursive)
    observer.start()

    logger.info(
        "Drive Defender watching %s (auto_quarantine=%s, recursive=%s, auto_update=%s)",
        target, auto_quarantine, recursive, auto_update,
    )

    last_check = time.time()
    try:
        while True:
            time.sleep(1)
            if auto_update and time.time() - last_check >= SIGNATURE_RECHECK_SECONDS:
                last_check = time.time()
                if update_signatures():
                    handler.signatures = load_signatures()
                    logger.info("Reloaded signatures after auto-update")
    except KeyboardInterrupt:
        logger.info("Stopping Drive Defender...")
        observer.stop()
    observer.join()
