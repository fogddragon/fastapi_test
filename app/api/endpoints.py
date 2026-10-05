import hashlib
import json

from app.schemas.schemas import UnprocessedDataSchema
from fastapi import APIRouter, Depends, HTTPException

from app.utils.data_transformer import transformer_function

from app.core.database import SessionDep
from app.models.models import CachedData
from app.core.database import get_db
from sqlmodel import Session, select

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

@router.post("/transform_list")
async def create_transform_list(data: UnprocessedDataSchema, db: Session = Depends(get_db)):
    data_dict = data.dict()
    hash = hashlib.md5(json.dumps(data_dict, sort_keys=True).encode("utf-8")).hexdigest()
    existed_data = db.exec(select(CachedData).where(CachedData.hash == hash)).all()
    if not existed_data:
        transformed_data = transformer_function(data_dict)
        cached_data = CachedData(
            hash=hash,
            data=transformed_data,
        )
        db.add(cached_data)
        db.commit()
        db.refresh(cached_data)

        return cached_data.id
    else:
        return existed_data[0].id


@router.get("/transform_list/{item_id}")
async def get_tansform_list(item_id: int, db: Session = Depends(get_db)):
    cached_data = db.get(CachedData, item_id)
    if not cached_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return cached_data.data
