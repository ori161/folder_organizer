# Folder Organizer

Smart File Organizer & Manager — a small Python GUI tool that cleans, deduplicates, and sorts the contents of a folder into category folders (photos, documents, audio, code, etc.).

## Features

- Graphical UI (PySide6) with three main actions:
  - **Organize Folder**: flattens nested folders, renames duplicate filenames, and moves files into category folders based on file extensions.
  - **Copy Folder**: copy the contents of one folder into another (preserves folder structure).
  - **Dry Run**: creates a copy of your folder and organizes it, so you can preview how your files will be organized without modifying the original folder.
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
- **"Organize Folder"** to select a folder and organize its contents.
- **"Copy Folder"** to copy a folder's contents to another destination.
- **"Dry Run"** to test how your folder will be organized without making permanent changes. A copy with `_dryrun` suffix is created and organized.

## How it works (high level)

### Organize Folder
1. The program traverses the selected folder and its subfolders.
2. Files are collected and duplicates are renamed with an incremental suffix (e.g. `file(1).txt`).
3. Files are categorized by extension according to `CATEGORY_CONFIG`.
4. Category directories are created inside the selected folder and files are moved into them.
5. Empty subfolders are removed after their files are moved up.

### Dry Run
1. Copies the selected folder to a new folder with `_dryrun` suffix (using Copy Folder internally).
2. Runs the organization process on the copy, leaving your original folder untouched.
3. Allows you to preview the results before organizing your actual folder.

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

- `main.py` — main application and organizing logic (GUI, file traversal, moving, renaming, dry run).
- `logger.py` — logging setup (writes `organizer.log` and prints select messages to console).
- `README.md` — this file.

## Logs

A log file named `organizer.log` is created in the working directory. It includes info/debug messages and exceptions to help diagnose issues.

## Safety & Tips

- The Organize action moves files (not copy) — make a backup or test on a sample folder first.
- Use the **Dry Run** feature to preview changes before organizing your actual folder.
- The Copy action uses `shutil.copytree(..., dirs_exist_ok=True)` to copy contents into a destination.
- Dry run folders are created with the `_dryrun` suffix and can be deleted after reviewing the results.

## Author

Created by ori161.
