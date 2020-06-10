import os
from fastapi import HTTPException


def create_chuck(filename: str):
    try:
        bytes = os.stat(filename).st_size
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found")

    if (bytes < 650):
        bytes = 650

    size = bytes // 3

    return size + 1
