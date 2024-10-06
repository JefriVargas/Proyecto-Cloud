import fastapi
import httpx
from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_db

from schemes.user import (
    UserCreate,
    UserAuth,
    UserResponse
)

from utils.user import (
    create_user,
    get_user_by_email,
    get_user_by_id
)

import bcrypt

router = fastapi.APIRouter()

@router.get('/')
async def index():
    return {'message': 'Hello World'}

@router.post(
    '/user/auth/signup',
    response_model=UserResponse
)
async def signup(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    db_result = await get_user_by_email(db, data.email)

    if db_result:
        raise HTTPException(status_code=406)

    new_user = await create_user(db, data)

    return UserResponse(
        user=new_user
    )

@router.post(
    '/user/auth/login',
    response_model=UserResponse
)
async def login(
    data: UserAuth,
    db: AsyncSession = Depends(get_db)
):
    db_result = await get_user_by_email(db, data.email)

    if not db_result:
        raise HTTPException(status_code=404)

    if not bcrypt.checkpw(
        data.password.encode('utf-8'),
        db_result.password.encode('utf-8')
    ):
        raise HTTPException(status_code=401)

    return UserResponse(
        user=db_result
    )

@router.get(
    '/user/{user_id}',
    response_model=UserResponse
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_result = await get_user_by_id(db, user_id)

    if not db_result:
        raise HTTPException(status_code=404, detail="User not found")

    async with httpx.AsyncClient() as client:
        achievements_response = await client.get(f"http://api2:8002/achievements/{user_id}")

    if achievements_response.status_code != 200:
        achievements_data = {}
        achievements_data['achievements'] = None
    else:
        achievements_data = achievements_response.json()

    return UserResponse(
        user=db_result,
        data={
            "achievements": achievements_data["achievements"]
        }
    )

@router.delete(
    '/user/{user_id}',
    response_model=UserResponse
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_result = await get_user_by_id(db, user_id)

    if not db_result:
        raise HTTPException(status_code=404)

    await db.delete(db_result)
    await db.commit()

    return UserResponse(
        user=db_result
    )

@router.patch(
    '/user/{user_id}',
    response_model=UserResponse
)
async def update_user(
    user_id: int,
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    db_result = await get_user_by_id(db, user_id)

    if not db_result:
        raise HTTPException(status_code=404)

    db_result.username = data.username
    db_result.email = data.email

    db_result.names = data.names
    db_result.lastnames = data.lastnames
    db_result.phone_number = data.phone_number
    db_result.age = data.age
    db_result.birthday = data.birthday

    await db.commit()

    return UserResponse(
        user=db_result
    )

