# Folder Organizer

Smart File Organizer & Manager — a small Python GUI tool that cleans, deduplicates, and sorts the contents of a folder into category folders (photos, documents, audio, code, etc.).

## Features

- Graphical UI (PySide6) with two main actions:
  - Organize Folder: flattens nested folders, renames duplicate filenames, and moves files into category folders based on file extensions.
  - Copy Folder: copy the contents of one folder into another (preserves folder structure).
- Configurable categories and extensions via `CATEGORY_CONFIG`.
- Safe renaming for duplicates (adds `(1)`, `(2)`, ... to filenames).
- Logging to `organizer.log` for troubleshooting and status messages.

## Quickstart

Requirements
- Python 3.8+
- PySide6

Recommended: use a virtual environment.

Install and run:

```bash
git clone https://github.com/ori161/folder_organizer.git
cd folder_organizer
python -m venv .venv
# Activate the venv (macOS / Linux)
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install PySide6
python main.py
```

The GUI window will open. Use:
- "Organize Folder" to select a folder and organize its contents.
- "Copy Folder" to copy a folder's contents to another destination.

## How it works (high level)

1. The program traverses the selected folder and its subfolders.
2. Files are collected and duplicates are renamed with an incremental suffix (e.g. `file(1).txt`).
3. Files are categorized by extension according to `CATEGORY_CONFIG`.
4. Category directories are created inside the selected folder and files are moved into them.
5. Empty subfolders are removed after their files are moved up.

## Configuration

Open `main.py` and edit the `CATEGORY_CONFIG` dictionary to add or change categories and their extensions. Example excerpt:

```python
CATEGORY_CONFIG = {
    'photos': ['.png', '.jpeg', '.jpg', '.gif', ...],
    'documents': ['.txt', '.pdf', '.docx', ...],
    ...
}
```

The code automatically inverts this mapping so extensions map to category names when organizing.

## Files & Structure

- `main.py` — main application and organizing logic (GUI, file traversal, moving, renaming).
- `logger.py` — logging setup (writes `organizer.log` and prints select messages to console).
- `README.md` — this file.

## Logs

A log file named `organizer.log` is created in the working directory. It includes info/debug messages and exceptions to help diagnose issues.

## Safety & Tips

- The Organize action moves files (not copy) — make a backup or test on a sample folder first.
- The Copy action uses `shutil.copytree(..., dirs_exist_ok=True)` to copy contents into a destination.
- If you want a "dry run" before moving files, you can modify the code to print planned moves instead of calling `shutil.move`.

## Author

Created by ori161.
