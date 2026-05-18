# assets
import os
import shutil

files_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf', '.docx', '.xlsx', '.txt', '.mp3', '.mp4', '.avi', '.mkv', '.zip', '.rar', '.7z', '.exe', '.dll', '.html', '.css', '.js', '.py', '.java', '.cpp',
                    '.c', '.h', '.php', '.rb', '.go', '.swift', '.ts', '.tsx']  # list of common file extensions not in work at the moment but might be useful in the future to sort the files into their designated folder.

name_of_files_set = set()  # global set to check names that already exist

# 1.----------move all files to parent folder---------------------------------------


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
                move_files(folder, subfolder)
                remove_folder(subfolder)
    return True

# 2.--------------micro functions---------------------------------------------------


def check_and_rename_files(parent_folder, current_file, type):  # will use a global set to check the file
    # names before moving files upward note: current file is not a path
    add_num_to_name = 1
    file_still_exist = True

    old_name = create_path(parent_folder, current_file)
    while file_still_exist:
        #new file name exists of the name of the file without the type + (number) + type
        new_file_name = current_file[:len(current_file)-len(type)] + f"({add_num_to_name})" + type
        print(new_file_name)
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


def move_files(folder, subfolder):
    if os.path.exists(subfolder):
        if os.listdir(subfolder):
            for f in os.listdir(subfolder):
                file_path = os.path.join(subfolder, f)
                shutil.move(file_path, folder)


# 3. ----------------------main func ------------------------------------------------
def main():
    # i will do few features like removing a file /folder with caution if some files are valuble //later 
    #organize folder by file type and move files to their designated folders and remove empty folders //already half done but not by file type yet
    #copy a file //can be done 
    #zip a folder// can be done 
    #rename a folder or a file // can be done need to remove the old name and add the new name to the set to prevent future conflicts 
    #when one folder organized and user eneded prog clear set and get ready for the next folder to organize //can be done
    #more ideas later
    folder = input("enter a folder to organize: ")

    if os.path.exists(folder):
        extract_all_files_and_remove_folders(folder)

    else:
        print("not a folder path!")


if __name__ == '__main__':
    main()