from typing import Annotated, Dict

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import Column, JSON
from sqlmodel import Field, Session, SQLModel, create_engine, select


class CachedData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(index=True, unique=True, max_length=40)
    data: Dict = Field(default_factory=dict, sa_column=Column(JSON))

    __table_args__ = {'extend_existing': True}

