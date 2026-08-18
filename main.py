# assets
import sys
import os
import shutil
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QFrame
)
from PySide6.QtCore import Qt

# logger
from logger import *
folder_organizer_logger = setup_logger()

CATEGORY_CONFIG = {
    'photos': ['.png', '.jpeg', '.jpg', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.heic'],
    'documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.rtf', '.pages', '.tex', '.md'],
    'spreadsheets': ['.xls', '.xlsx', '.ods', '.csv', '.tsv'],
    'presentations': ['.ppt', '.pptx', '.odp', '.key'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', '.aiff', '.m4r'],
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
    'code': ['.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.c', '.cpp', '.h', '.java', '.rs',
             '.go', '.php', '.rb', '.sh', '.sql'],
    'executables': ['.exe', '.msi', '.app', '.deb', '.rpm', '.dmg', '.bin'],
    'fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot']
}

# databases

files_extension_by_group = {}
name_of_files_set = set()
sort_files = {}
files_to_folders = {}


# ------------managing class---------------------------------------------------------------------

class FolderOrganizerManager:
    def __init__(self):
        invert_Files_extension_by_group(CATEGORY_CONFIG) # invert category config so the key is the extension
        # and the value os which folder this extension will be in later

    # 1.--------------organize folder method------------------------
    def organize_folder(self, screen):
        try:
            folder = QFileDialog.getExistingDirectory(screen, "Select a folder to organize")
            if not folder:
                return "Operation cancelled."

            if os.path.exists(folder):
                folder_organizer_logger.info(f"starting organization for {folder}...")
                extract_all_files_and_remove_folders(folder)
                dictionary_files_keys_to_types_values(folder)
                sort_files_to_folders()
                move_files_to_folders(folder)

                # clear "data bases" per use.
                folder_organizer_logger.info("clearing databases...")
                name_of_files_set.clear()
                sort_files.clear()
                files_to_folders.clear()
                folder_organizer_logger.info("folder was successfully organized")
                return "Successfully organized folder!"
            else:
                folder_organizer_logger.warning("folder does not exist")
                return f"Folder does not exist: {folder}"
        except PermissionError:
            folder_organizer_logger.error("Error: Permission denied while accessing files.")
            return "Error: Permission denied while accessing files."
        except Exception as e:
            folder_organizer_logger.exception(f"unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"

    # 2.--------------copy folder method-----------------------------
    def copy_folder(self, screen):
        try:
            src = QFileDialog.getExistingDirectory(screen, "Select a folder to copy")
            if not src:
                folder_organizer_logger.warning("operation cancelled src is null")
                return "Operation cancelled."
            if not os.path.exists(src):
                folder_organizer_logger.warning(f"{src} does not exist")
                return f"The source path does not exist: {src}"
            if os.path.isfile(src):
                folder_organizer_logger.info(f"the selected src is a file: {src}")
                return f"The selected source is a file, not a folder."

            dst = QFileDialog.getExistingDirectory(screen, "Select destination folder")
            if not dst:
                folder_organizer_logger.warning("operation cancelled dst is null")
                return "Operation cancelled."

            folder_organizer_logger.info(f"making folder {dst} if not already exists...")
            os.makedirs(dst, exist_ok=True)

            folder_organizer_logger.info(f"copying {src} to {dst}...")
            shutil.copytree(src, dst, dirs_exist_ok=True)
            folder_organizer_logger.info(f"{src} copied successfully to {dst}")
            return f"Successfully copied folder contents."
        except PermissionError:
            folder_organizer_logger.error("Permission denied during copy operation.")
            return "Error: Permission denied during copy operation."
        except Exception as e:
            folder_organizer_logger.exception(f"Error: {e}")
            return f"Error: {e}"


class FileOrganizerGui(QWidget):
    def __init__(self):
        super().__init__()
        self.methods = FolderOrganizerManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart File Organizer")
        self.resize(650, 500)

        # used an ai to help me make a modern style
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#TitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #0f172a;
            }
            QLabel#SubtitleLabel {
                font-size: 14px;
                color: #64748b;
            }
            QLabel#StatusLabel {
                font-size: 13px;
                color: #0284c7;
                background-color: #e0f2fe;
                border: 1px solid #bae6fd;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 24px;
                min-width: 220px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QFrame#Card {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Header Section
        title_label = QLabel("File Organizer & Manager")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("Clean up your directories or back up folders efficiently.")
        subtitle_label.setObjectName("SubtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addSpacing(10)

        # Center Card Frame for Actions
        card_frame = QFrame()
        card_frame.setObjectName("Card")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)

        # Buttons
        self.button_folder_organizer = QPushButton("Organize Folder")
        self.button_folder_organizer.clicked.connect(lambda: self.handle_action(self.methods.organize_folder))

        self.button_copy_folder = QPushButton("Copy Folder")
        self.button_copy_folder.clicked.connect(lambda: self.handle_action(self.methods.copy_folder))

        card_layout.addWidget(self.button_folder_organizer, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.button_copy_folder, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(card_frame)

        # Status / Feedback label
        self.info_label = QLabel("Ready. Choose an option above to begin.")
        self.info_label.setObjectName("StatusLabel")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)
        main_layout.addWidget(self.info_label)

    def handle_action(self, method):
        result_action = method(self)
        self.info_label.setText(result_action)


# ----------methods for folder clean and organize feature---------------------------------------


def extract_all_files_and_remove_folders(folder):
    try:
        if not os.listdir(folder):
            remove_folder(folder)
            return False

        items = os.listdir(folder)
        for f in items:
            file_path = create_path(folder, f)
            if os.path.isfile(file_path):
                if f in name_of_files_set:
                    _, ext = os.path.splitext(f)
                    check_and_rename_files(folder, f, ext)
                else:
                    name_of_files_set.add(f)

        for f in items:
            subfolder = create_path(folder, f)
            if os.path.isdir(subfolder):
                flag = extract_all_files_and_remove_folders(subfolder)
                if flag:
                    move_all_files_from_folder(folder, subfolder)
                    remove_folder(subfolder)
        return True
    except Exception as e:
        folder_organizer_logger.exception(f"Error processing folder structure: {e}")
        print(f"Error processing folder structure: {e}")
        return False


def dictionary_files_keys_to_types_values(folder):
    try:
        for file in os.listdir(folder):
            file_path = create_path(folder, file)

            if os.path.isdir(file_path):
                continue

            _, extension = os.path.splitext(file)
            extension = extension.lower()

            if extension in files_extension_by_group.keys():
                sort_files[file] = extension
    except Exception as e:
        folder_organizer_logger.exception(f"Error reading file types: {e}")
        print(f"Error reading file types: {e}")


def sort_files_to_folders():
    for file, ext in sort_files.items():
        files_to_folders[file] = files_extension_by_group[ext]


def move_files_to_folders(main_folder):
    for file, folder in files_to_folders.items():
        try:
            file_path = create_path(main_folder, file)
            folder_path = create_path(main_folder, folder)
            os.makedirs(folder_path, exist_ok=True)
            move_single_file(file_path, folder_path)
        except Exception as e:
            folder_organizer_logger.exception(f"Could not move file {file}: {e}")
            print(f"Could not move file {file}: {e}")


def invert_Files_extension_by_group(dictionary):
    for key, value in dictionary.items():
        for ext in value:
            files_extension_by_group[ext] = key


# --------------micro methods---------------------------------------------------

def check_and_rename_files(parent_folder, current_file, type):
    add_num_to_name = 1
    file_still_exist = True

    old_name = create_path(parent_folder, current_file)
    while file_still_exist:
        new_file_name = current_file[:len(current_file) - len(type)] + f"({add_num_to_name})" + type
        if new_file_name not in name_of_files_set:
            new_name = create_path(parent_folder, new_file_name)
            rename_file(old_name, new_name)
            name_of_files_set.add(new_file_name)
            file_still_exist = False
        add_num_to_name += 1


def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
    except Exception as e:
        folder_organizer_logger.exception(f"Error renaming file: {e}")
        print(f"Error renaming file: {e}")


def create_path(folder, file):
    return os.path.join(folder, file)


def remove_folder(folder):
    try:
        os.rmdir(folder)
    except Exception as e:
        folder_organizer_logger.exception(f"Error removing empty folder {folder}: {e}")
        print(f"Error removing empty folder {folder}: {e}")


def move_all_files_from_folder(folder, subfolder):
    try:
        if os.path.exists(subfolder):
            if os.listdir(subfolder):
                for f in os.listdir(subfolder):
                    file_path = os.path.join(subfolder, f)
                    shutil.move(file_path, folder)
    except Exception as e:
        folder_organizer_logger.exception(f"Error moving files from subfolder: {e}")
        print(f"Error moving files from subfolder: {e}")


def move_single_file(file, dest_folder):
    try:
        shutil.move(file, dest_folder)
    except Exception as e:
        folder_organizer_logger.exception(f"Error moving file {file}: {e}")
        print(f"Error moving file {file}: {e}")


# 3. ----------------------main func ------------------------------------------------


def main():
    app = QApplication(sys.argv)
    window = FileOrganizerGui()
    window.show()

    folder_organizer_logger.info("running program...")
    run = app.exec()
    folder_organizer_logger.info("ending program...")
    sys.exit(run)


if __name__ == '__main__':
    main()
