import os


def chuckSize(filename):
    bytes = os.stat(filename).st_size
    if (bytes < 650):
        bytes = 650

    size = bytes // 30

    return size + 1
