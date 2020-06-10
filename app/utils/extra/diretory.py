import os


def remove_create(file_id: str):
    try:
        os.remove(f'./documents/{file_id}.mp4')
    except FileNotFoundError:
        pass

    try:
        os.mkdir('./temp')
    except FileExistsError:
        pass

    try:
        os.mkdir('documents')
    except FileExistsError:
        pass
