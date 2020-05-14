import glob
import mimetypes
import os


def create_filename(direName, fileName, minetype):
    type = mimetypes.guess_extension(minetype)
    if type:
        filename = f'{direName}/{fileName}{type}'
    else:
        filename = f'{direName}/{fileName}.unknow'
    return filename


def create_new_dir(dirName, specific_dir):
    dir = './Chat'
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    try:
        os.mkdir(dirName)
    except FileExistsError:
        pass

    if specific_dir:
        try:
            specific_dir = f'{dirName}/{specific_dir}'
            os.mkdir(specific_dir)
        except FileExistsError:
            pass

        return specific_dir

    return dirName


def exit_files(dirName, filename, mimetype):
    type = mimetypes.guess_extension(mimetype)
    if type:
        type
    else:
        type = '.unknow'
    path_to_file_list = glob.glob(dirName + '*' + type)
    for path_to_file in path_to_file_list:
        if path_to_file == filename:
            return False
    return True
