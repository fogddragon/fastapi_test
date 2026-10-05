from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Session

from . import config


postgres_url =f"postgresql+psycopg2://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}/{config.DATABASE_NAME}"


engine = create_engine(postgres_url)


def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
