from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, delete, update

from models.models import kitten
from kitten.schemas import Kitten, KittenEdit


router = APIRouter()

@router.get("/", summary="Возвращает всех котят", response_model=list[Kitten])
async def get_kiten(session : AsyncSession = Depends(get_async_session)):
    query = select(kitten)
    result = await session.execute(query)
    return result.all()

@router.get("/{id}", summary="Возвращает котят с указанным id породы", response_model=list[Kitten])
async def get_user_by_id(id: int, session : AsyncSession = Depends(get_async_session)):
    query = select(kitten).where(kitten.c.breedID == id)
    result = await session.execute(query)
    return result.all()

@router.post("/", summary="Добавить котёнка")
async def post_addkitten(data: KittenEdit, session : AsyncSession = Depends(get_async_session)):
    query = insert(kitten).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.put("/{id}", summary="Изменение информации о котёнке с указанным id")
async def get_user_by_id(id: int, data: KittenEdit, session : AsyncSession = Depends(get_async_session)):
    query = update(kitten).where(kitten.c.kittenID == id).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.delete("/{id}", summary="Удаляет котёнка по id")
async def delete_kitten(id: int, session : AsyncSession = Depends(get_async_session)):
    query = delete(kitten).where(kitten.c.kittenID == id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}