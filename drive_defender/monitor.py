import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import config
from .logger import get_logger
from .quarantine import quarantine_file

logger = get_logger()


def is_suspicious(path: Path) -> bool:
    if path.name.lower() in config.SUSPICIOUS_FILENAMES:
        return True
    return path.suffix.lower() in config.SUSPICIOUS_EXTENSIONS


class DriveDefenderHandler(FileSystemEventHandler):
    def __init__(self, auto_quarantine: bool = False):
        super().__init__()
        self.auto_quarantine = auto_quarantine

    def _handle(self, event_type: str, src_path: str):
        path = Path(src_path)
        if path.is_dir():
            return

        if is_suspicious(path):
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


def watch(drive: str = config.DEFAULT_DRIVE, auto_quarantine: bool = False, recursive: bool = True):
    target = Path(drive)
    if not target.exists():
        logger.error("Drive/path does not exist: %s", target)
        return

    handler = DriveDefenderHandler(auto_quarantine=auto_quarantine)
    observer = Observer()
    observer.schedule(handler, str(target), recursive=recursive)
    observer.start()

    logger.info(
        "Drive Defender watching %s (auto_quarantine=%s, recursive=%s)",
        target, auto_quarantine, recursive,
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping Drive Defender...")
        observer.stop()
    observer.join()
