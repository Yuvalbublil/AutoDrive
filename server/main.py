import os
import sys
import time

MAX_DUPLICATES = 20

TMP_DRIVEDOWNLOAD = [".tmp.drivedownload", ".tmp.driveupload"]
import logging


def check_folder_empty(folder_path):
    """
    Check if a folder is empty
    :param folder_path: path to folder
    :return:
    """
    if not os.listdir(folder_path) or os.listdir(folder_path) == [TMP_DRIVEDOWNLOAD]:
        return True
    else:
        return False


def handle_duplicate_files(drive_folder_path, nas_folder_path, file_name):
    """
    Handle duplicate files
    add number to the end of file name
    :param drive_folder_path:
    :param nas_folder_path:
    :param file_name:
    :return:
    """


def move_content(folder_path, new_folder_path, exclude_list=[]):
    """
    Move all content from one folder to another
    :param folder_path: path to folder
    :param new_folder_path: path to new folder
    :return:
    """
    count = 0
    for file in os.listdir(folder_path):
        if file not in exclude_list:

            if not os.path.exists(os.path.join(new_folder_path, file)):
                logging.debug(f"Moving {file}")
                os.rename(os.path.join(folder_path, file), os.path.join(new_folder_path, file))
                count += 1
            elif os.path.isfile(os.path.join(folder_path, file)):
                i = 1
                while i < MAX_DUPLICATES:
                    name_tup = os.path.splitext(file)
                    temp_name= f"{name_tup[0]} ({i}){name_tup[1]}"
                    if not os.path.exists(os.path.join(new_folder_path, temp_name)):
                        os.rename(os.path.join(folder_path, file), os.path.join(new_folder_path, temp_name))
                        logging.debug(f"Moving {temp_name}")
                        break
                    else:
                        i += 1
                count += 1

            if os.path.isdir(os.path.join(folder_path , file)):
                # logging.debug(f"Entering {file}")
                count += move_content(os.path.join(folder_path, file), os.path.join(new_folder_path, file),
                                      exclude_list)
    return count


def check_folder_exists(folder_path):
    """
    Check if a folder exists
    :param folder_path: path to folder
    :return:
    """
    if os.path.exists(folder_path):
        return True
    else:
        return False


def refactor_path(path):
    """
    Refactor path to add trailing slash
    :param path: path to refactor
    :return: refactored path
    """
    if path[-1] == '\\':
        return path
    else:
        return path + "\\"


def main():
    init_logger()
    # drive_folder_path = refactor_path(input("Enter Drive folder path: "))
    # nas_folder_path = refactor_path(input("Enter NAS folder path: "))
    # time_per_cycle = int(input("Enter time per cycle in seconds: "))
    drive_folder_path = refactor_path("./Temp Our Pictures")
    nas_folder_path = refactor_path("./Temp NAS")
    drive_folder_path = "./Temp Our Pictures"
    nas_folder_path = "./Temp NAS"
    time_per_cycle = 20
    while (True):
        move_to_nas(drive_folder_path, nas_folder_path, verbose=True)
        create_dirtree_without_files(nas_folder_path, drive_folder_path)
        time.sleep(time_per_cycle)


def init_logger():
    date_strftime_format = "%d-%b-%Y %H:%M:%S"
    message_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="drive_to_nas.log", level=logging.INFO, format=message_format,
                        datefmt=date_strftime_format)
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=message_format,
    #                     datefmt=date_strftime_format)


def move_to_nas(drive_folder_path, nas_folder_path, verbose=True):
    if check_folder_exists(drive_folder_path):
        if check_folder_empty(drive_folder_path):
            if verbose:
                logging.info("Drive folder is empty")
        else:
            if check_folder_exists(nas_folder_path):
                if check_folder_empty(nas_folder_path):
                    if verbose:
                        logging.info("NAS folder is empty")
                else:
                    num = move_content(drive_folder_path, nas_folder_path, exclude_list=TMP_DRIVEDOWNLOAD)
                    if verbose:
                        logging.info(f"Moved content from Drive to NAS - {num} files")
            else:
                if verbose:
                    logging.info("NAS folder does not exist")
    else:
        if verbose:
            logging.info("Drive folder does not exist")


def walk_tree():
    # importing the shutil module
    import shutil

    # importing the os module
    import os

    # defining the function to ignore the files
    # if present in any folder
    def ignore_files(dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f))]

    shutil.copytree(r"C:\Users\t8864522\CLionProjects",
                    'copied_structure',
                    ignore=ignore_files)


# defining a function for the task
def create_dirtree_without_files(src, dst):
    # getting the absolute path of the source
    # directory
    src = os.path.abspath(src)

    # making a variable having the index till which
    # src string has directory and a path separator
    src_prefix = len(src) + len(os.path.sep)

    # making the destination directory
    try:
        os.makedirs(dst)
    except FileExistsError:
        pass
    changed = False
    # doing os walk in source directory
    for root, dirs, files in os.walk(src):
        for dirname in dirs:
            # here dst has destination directory,
            # root[src_prefix:] gives us relative
            # path from source directory
            # and dirname has folder names
            dirpath = os.path.join(dst, root[src_prefix:], dirname)

            # making the path which we made by
            # joining all of the above three
            try:
                os.mkdir(dirpath)
                changed = True
            except FileExistsError:
                pass
    if changed:
        logging.info("Directory structure created")


# calling the above function


if __name__ == '__main__':
    # create_dirtree_without_files(r"C:\Users\t8864522\CLionProjects",
    #                              'copied_structure')
    # walk_tree()
    main()
