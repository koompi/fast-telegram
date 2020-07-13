import glob
import os


def is_not_exit(dirName, filename,  mimetype):
    create_dir(dirName)
    path_to_file_list = glob.glob(dirName + '*' + mimetype)
    for path_to_file in path_to_file_list:
        if path_to_file == filename:
            return False
    return True


def create_dir(dirName):
    try:
        os.mkdir(dirName)
    except FileExistsError:
        pass
