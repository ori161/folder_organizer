# assets
import os
import shutil


def extract_all_files_and_remove_folders(folder): # might use the while inside a recursive func
    if not os.listdir(folder): # if subfolder is empty then remove immidiatly
        remove_folder(folder)
        return False

    items = os.listdir(folder)
    for f in items:
        if os.path.isdir(create_path(folder, f)):
            subfolder = create_path(folder, f)

            flag = extract_all_files_and_remove_folders(subfolder)
            if flag:
                # a func that checks name with a global set to prevent two files with the same name
                move_files(folder, subfolder)
                remove_folder(subfolder)
    return True


def check_and_rename_files(current_folder): # will use a global set to check the file names before moving files upward
    pass


def create_path(folder, file):
    return os.path.join(folder, file)


def remove_folder(folder):
    os.rmdir(folder)


def move_files(folder, subfolder):
    if os.path.exists(subfolder):
        if os.listdir(subfolder):
            for f in os.listdir(subfolder):
                file_path = os.path.join(subfolder, f)
                shutil.move(file_path, folder)


def main():
    folder = input("enter a folder to organize: ")

    if os.path.exists(folder):
        extract_all_files_and_remove_folders(folder)

    else:
        print("not a folder path!")


if __name__ == '__main__':
    main()
