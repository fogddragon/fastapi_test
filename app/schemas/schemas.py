from typing import List

from pydantic import BaseModel


class UnprocessedDataSchema(BaseModel):
    list_1: List[str]
    list_2: List[str]


class ProcessedDataSchema(BaseModel):
    output: List[str]
