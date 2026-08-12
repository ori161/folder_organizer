# assets
import sys
import os
import shutil
from collections import defaultdict
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox


CATEGORY_CONFIG = {
    'photos': ['.png', '.jpeg', '.jpg', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.heic'],
    'documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.rtf', '.pages', '.tex', '.md'],
    'spreadsheets': ['.xls', '.xlsx', '.ods', '.csv', '.tsv'],
    'presentations': ['.ppt', '.pptx', '.odp', '.key'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', '.aiff', '.m4r'],
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
    'code': ['.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.c', '.cpp', '.h', '.java', '.rs', '.go', '.php', '.rb', '.sh', '.sql'],
    'executables': ['.exe', '.msi', '.app', '.deb', '.rpm', '.dmg', '.bin'],
    'fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot']
} # here a programmer can add more categories and their extensions to sort files by type and move them to their designated folders

files_extension_by_group = {} # this is what used in the code after we invert the category_config dictionary, it will look like this: {'.png': 'photos', '.jpeg': 'photos', '.jpg': 'photos', '.gif': 'photos', '.bmp': 'photos', '.tiff': 'photos', '.webp': 'photos'} 

name_of_files_set = set()  # global set to check names that already exist

sort_files = {} # dictionary to sort files by keys
files_to_folders = {}


# ------------managing class---------------------------------------------------------------------

class FileOrganizerManager():
    def __init__(self):
        invert_Files_extension_by_group()


    # 1.--------------organize folder method------------------------
    def organize_file(self):
        
        folder = input("enter a folder to organize: ")

        if os.path.exists(folder):
            flag_method_one = False
            extract_all_files_and_remove_folders(folder)
            dictionary_files_keys_to_types_values(folder)
            sort_files_to_folders()
            move_files_to_folders(folder)
        else:
            raise(f"folder: {folder} does not exist.")


    # 2.--------------copy folder method-----------------------------
    def copy_folder(src, dst):
        try:
            if not os.path.exists():
                raise(f"the source {src} does not exist")
            if os.path.isfile():
                raise(f"the source {src} is a file and not an folder")

            os.mkdirs(dst, exist_ok=True) # make a folder if it does not exist (dst is a full path user needs to choose where to copy to)

            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"a copy of {src} is now in {dst}.")
        except Exception as e:
            print(f"Error: {e}")


    # 3.--------------zip_folder method------------------------------
    def zip_folder(src):
        try:
            if not os.path.exists():
                raise(f"the source {src} does not exist")
            if os.path.isfile():
                raise(f"the source {src} is a file and not an folder")
        
            zip_name = shutil._make_zipfile(os.path.basename(src), src)
            print(f"{zip_name} was succesfully created.")

        except Exception as e:
            print(f"Error: {e}")


class FileOrganizerGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("file organizer")
        self.showMaximized()

        screen = QVBoxLayout()


#----------methods for folder clean and organize feature---------------------------------------


def extract_all_files_and_remove_folders(folder):  # might use the while inside a recursive func
    if not os.listdir(folder): # if subfolder is empty then remove immediately and return false to prevent the program collapse.
        remove_folder(folder)
        return False

    items = os.listdir(folder)
    #check if a file already exists in parent folder and rename before even cleaning the next folder to prevent name conflicts
    for f in items:
        if os.path.isfile(create_path(folder, f)):
            if f in name_of_files_set:
                _, ext = os.path.splitext(f)
                check_and_rename_files(folder, f, ext)
            else:
                name_of_files_set.add(f)
    
    # after moving all files to the parent folder we will check for subfolders and remove them
    for f in items:
        if os.path.isdir(create_path(folder, f)):
            subfolder = create_path(folder, f)

            flag = extract_all_files_and_remove_folders(subfolder)
            if flag:
                # a func that checks name with a global set to prevent two files with the same name
                move_all_files_from_folder(folder, subfolder)
                remove_folder(subfolder)
    return True


def dictionary_files_keys_to_types_values(folder):
    # basically just iterate through the main folder and sort the files
    # by their extension for later method to sort it to organized folders
    for file in os.listdir(folder):
        if not os.path.isdir(file):
            _,extension = os.path.splitext(file)

            sort_files[file] = extension # add to dictionary


def sort_files_to_folders(): # initiate a dictionary that has the file as a key and the name of the folder it belongs to as a value: {example.jpg : "pictures"...}
    for file, ext in sort_files.items():
        files_to_folders[file] = files_extension_by_group[ext]


def move_files_to_folders(main_folder):
    for file, folder in files_to_folders.items():
        file_path = create_path(main_folder, file)
        folder_path = create_path(main_folder, folder)
        if(not os.path.exists(folder_path)):
            os.makedirs(folder_path, exist_ok=True)
        move_single_file(file_path, folder_path)


# helper fuction that flips the category_config key value(intends to be friendly when adding a lot of new extensions)
def invert_Files_extension_by_group(dictionary=CATEGORY_CONFIG):
    for key, value in dictionary.items():
        for ext in value:
            files_extension_by_group[ext] = key


#--------------micro methods---------------------------------------------------

def check_and_rename_files(parent_folder, current_file, type):  # will use a global set to check the file
    # names before moving files upward note: current file is not a path
    add_num_to_name = 1
    file_still_exist = True

    old_name = create_path(parent_folder, current_file)
    while file_still_exist:
        #new file name exists of the name of the file without the type + (number) + type
        new_file_name = current_file[:len(current_file)-len(type)] + f"({add_num_to_name})" + type
        if new_file_name not in name_of_files_set:
            # create a path for the new name to rename the file and add the new name to the set to prevent future conflicts
            new_name = create_path(parent_folder, new_file_name)
            rename_file(old_name, new_name)
            name_of_files_set.add(new_file_name)
            file_still_exist = False
        add_num_to_name += 1


def rename_file(old_name, new_name):  # the name means an entire path!!!
    os.rename(old_name, new_name)


def create_path(folder, file):
    return os.path.join(folder, file)


def remove_folder(folder):
    os.rmdir(folder)


def move_all_files_from_folder(folder, subfolder):
    if os.path.exists(subfolder):
        if os.listdir(subfolder):
            for f in os.listdir(subfolder):
                file_path = os.path.join(subfolder, f)
                shutil.move(file_path, folder)


def move_single_file(file, dest_folder):
    shutil.move(file, dest_folder)


# 3. ----------------------main func ------------------------------------------------


def main():
   #task: finish the gui/ exceptions/ managment class

    # when one folder organized and user eneded prog clear set and get
    # ready for the next folder to organize //can be done
    
    # method 1
    #folder_managment()
    # when method one is needed again erase the sets and all the stuff that holds memories

    app = QApplication(sys.argv)
    window = FileOrganizerGui()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

