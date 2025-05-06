from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert, delete

from models.models import breed
from breed.schemas import Breed, BreedAdd

router = APIRouter()

@router.get("/", summary="Возвращает все породы", response_model=list[Breed])
async def get_breed(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    query = select(breed).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

@router.post("/", summary="Добавить породу")
async def post_addbreed(data: BreedAdd, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(breed).values(**data.model_dump())
        await session.execute(query)
        await session.commit()
        return {"status": "success"}
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Не удалось добавить породу")

@router.delete("/{id}", summary="Удаляет породу по id")
async def delete_breed(id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(breed).where(breed.c.breedID == id)
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Порода не найдена")
    return {"status": "success"}