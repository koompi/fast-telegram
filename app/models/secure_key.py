from pydantic import BaseModel


class Generate(BaseModel):
    password: str = None
    force_gen: bool = False
