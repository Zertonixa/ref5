from fastapi import APIRouter, Depends, HTTPException
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database import get_async_session
from sqlalchemy import select, insert, delete, update
from ..cache import redis_client

from models.models import kitten
from kitten.schemas import Kitten, KittenEdit


router = APIRouter()

@router.get("/", summary="Возвращает всех котят", response_model=list[Kitten])
async def get_kittens(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    cache_key = f"kittens:skip={skip}:limit={limit}"
    
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    query = select(kitten).offset(skip).limit(limit)
    result = await session.execute(query)
    kittens = result.scalars().all()
    
    kittens_data = [k.dict() for k in kittens]
    
    await redis_client.setex(cache_key, 300, json.dumps(kittens_data))
    
    return kittens_data

@router.get("/{id}", summary="Возвращает котёнка с указанным id", response_model=Kitten)
async def get_kitten_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(kitten).where(kitten.c.kittenID == id)
    result = await session.execute(query)
    kitten_obj = result.scalar_one_or_none()
    if not kitten_obj:
        raise HTTPException(status_code=404, detail="Котёнок не найден")
    return kitten_obj

@router.get("/by_breed/{breed_id}", summary="Возвращает котят указанной породы", response_model=list[Kitten])
async def get_kittens_by_breed(breed_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(kitten).where(kitten.c.breedID == breed_id)
    result = await session.execute(query)
    return result.scalars().all()

@router.post("/", summary="Добавить котёнка")
async def post_add_kitten(data: KittenEdit, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(kitten).values(**data.model_dump())
        await session.execute(query)
        await session.commit()
        return {"status": "success"}
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Не удалось добавить котёнка")

@router.put("/{id}", summary="Изменение информации о котёнке с указанным id")
async def put_update_kitten(id: int, data: KittenEdit, session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(kitten).where(kitten.c.kittenID == id).values(**data.model_dump())
        result = await session.execute(query)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Котёнок не найден для обновления")
        return {"status": "success"}
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Не удалось обновить котёнка")

@router.delete("/{id}", summary="Удаляет котёнка по id")
async def delete_kitten(id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(kitten).where(kitten.c.kittenID == id)
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Котёнок не найден для удаления")
    return {"status": "success"}