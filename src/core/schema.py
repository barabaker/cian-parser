import ast
from typing import List
from pydantic import BaseModel, field_validator


class Subject(BaseModel):
    id: List[int]
    name: str
    bbox: List[List[float]]
    offer_type: str

    @field_validator('bbox', mode='before')
    def parse_bbox(cls, value: str) -> List[List[float]]:
        if isinstance(value, str):
            return ast.literal_eval(value)



class Work(BaseModel):
    page: int = 1
    subject_id: List[int]
    bbox: List[List[float]]
    offer_type: str

