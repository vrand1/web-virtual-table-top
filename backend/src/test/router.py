from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

router = APIRouter()

class ValidationModel(BaseModel):
    name: str
    age: int
#regin test_router
@router.get("/info")
async def test_info():
    """Проверка обычного успешного лога."""
    logger.info("Тестовая ручка")
    return {"status": "ok", "detail": "Работает"}

@router.get("/error-500")
async def test_crash():
    """Проверка перехвата фатальной ошибки (DivisionByZero)."""
    return 1 / 0

@router.post("/error-422")
async def test_validation(data: ValidationModel):
    """Проверка ошибки валидации Pydantic."""
    return data

@router.get("/error-db")
async def test_db_error():
    """Имитация ошибки базы данных"""
    from sqlalchemy.exc import IntegrityError
    raise IntegrityError("select * from non_existing_table", params={}, orig=Exception("Table not found"))

#end region test_router