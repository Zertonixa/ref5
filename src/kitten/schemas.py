from pydantic import BaseModel

class Kitten(BaseModel):
    kittenID: int
    name: str
    breedID: int
    age: int
    color: str
    description: str

class KittenEdit(BaseModel):
    name: str
    breedID: int
    age: int
    color: str
    description: str