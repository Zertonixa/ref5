from pydantic import BaseModel

class Breed(BaseModel):
    breedID: int
    description: str
    origin: str

class BreedAdd(BaseModel):
    description: str
    origin: str