from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, delete, update

from models.models import kitten
from kitten.schemas import Kitten, KittenAdd


router = APIRouter()

@router.get("/", summary="Возвращает всех котят", response_model=list[Kitten])
async def get_kiten(session : AsyncSession = Depends(get_async_session)):
    # query = user.select()
    query = select(kitten)
    result = await session.execute(query)
    return result.all()

@router.post("/", summary="Добавить котёнка")
async def post_addkitten(data: KittenAdd, session : AsyncSession = Depends(get_async_session)):
    query = insert(kitten).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.delete("/{id}", summary="Удаляет котёнка по id")
async def delete_kitten(id: int, session : AsyncSession = Depends(get_async_session)):
    query = delete(kitten).where(kitten.c.kittenID == id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}