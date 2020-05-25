import os


def chuckSize(filename):
    filesize = os.stat(filename).st_size
    chunksize = (filesize // 2) + 1
