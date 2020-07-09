from pydantic import BaseModel


class Generate(BaseModel):
    force_gen: bool = False


class BuyKey(BaseModel):
    file_id: str
    expire: int = 7
