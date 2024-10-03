from pydantic import BaseModel

class Kitten(BaseModel):
    kittenID: int
    name: str
    age: str
    color: str
    description: str

class KittenAdd(BaseModel):
    name: str
    age: str
    color: str
    description: str