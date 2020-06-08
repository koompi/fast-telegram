from pydantic import BaseModel


class Generate(BaseModel):
    password: str
    force_gen: bool = False
