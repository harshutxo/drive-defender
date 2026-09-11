# drive-defender

A real-time file monitor for Windows that watches a drive or folder and flags — or optionally quarantines — suspicious files as they appear.

Built on [`watchdog`](https://pypi.org/project/watchdog/), it runs continuously in the background, checking new and changed files against a set of signatures (suspicious extensions/filenames). Signatures auto-update from this repository on an interval, with room for your own custom additions layered on top.

## Features

- Real-time, recursive (or top-level-only) monitoring of a target drive/folder
- Optional automatic quarantine of files that match a suspicious signature
- Signatures auto-refresh from GitHub on a configurable interval, or on demand
- User-maintained custom signature list merged on top of the bundled/remote set
- Simple CLI, no configuration file required to get started

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Watch the default drive (D:\), just log suspicious files
python main.py

# Watch a specific drive and auto-quarantine matches
python main.py --drive E:\ --quarantine

# Only watch the top level, skip subfolders
python main.py --no-recursive

# Force-refresh signatures from GitHub right now
python main.py --update-signatures
```

| Flag | Description |
|---|---|
| `--drive PATH` | Drive or folder to watch (default: `D:\`) |
| `--quarantine` | Automatically move suspicious files to the quarantine folder |
| `--no-recursive` | Only watch the top-level directory |
| `--no-auto-update` | Don't check GitHub for updated signatures |
| `--update-signatures` | Force-fetch the latest signatures now and exit |

Logs and quarantined files are kept under `~/.drive_defender/`.

## Support this project

If drive-defender is useful to you, consider [sponsoring it on GitHub](https://github.com/sponsors/harshutxo).
