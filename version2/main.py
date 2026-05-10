# assets
import os
import shutil

name_of_files_set = set()  # global set to check names that already exist

# 1.----------move all files to parent folder---------------------------------------


def extract_all_files_and_remove_folders(folder):  # might use the while inside a recursive func
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
        else:
            if f in name_of_files_set:
                check_and_rename_files(items, f)
            else:
                name_of_files_set.add(f)

    return True

# 2.--------------micro functions---------------------------------------------------


def check_and_rename_files(parent_folder, current_file):  # will use a global set to check the file
    # names before moving files upward note: current file is not a path
    add_num_to_name = 1
    file_still_exist = True

    old_name = create_path(parent_folder, current_file)
    while file_still_exist:
        new_file_name = current_file + f"({add_num_to_name})"
        if new_file_name not in name_of_files_set:
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


def move_files(folder, subfolder):
    if os.path.exists(subfolder):
        if os.listdir(subfolder):
            for f in os.listdir(subfolder):
                file_path = os.path.join(subfolder, f)
                shutil.move(file_path, folder)


# 3. ----------------------main func ------------------------------------------------
def main():
    folder = input("enter a folder to organize: ")

    if os.path.exists(folder):
        extract_all_files_and_remove_folders(folder)

    else:
        print("not a folder path!")


if __name__ == '__main__':
    main()
