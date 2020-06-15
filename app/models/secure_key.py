from pydantic import BaseModel


class Generate(BaseModel):
    password: str = None
    force_gen: bool = False


class BuyKey(BaseModel):
    file_id: str
    expire: int = 7
