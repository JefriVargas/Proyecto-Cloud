from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user import (
    User,
    UserData
)

from schemes.user import (
    UserCreate
)

import bcrypt

async def create_user(
    db: AsyncSession,
    user: UserCreate
):

    password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=password.decode('utf-8')
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    new_user_data = UserData(
        user=new_user,
        names=user.names,
        lastnames=user.lastnames,
        phone_number=user.phone_number,
        age=user.age,
        birthday=user.birthday
    )

    db.add(new_user_data)
    await db.commit()
    await db.refresh(new_user_data)

    new_user.names = new_user_data.names
    new_user.lastnames = new_user_data.lastnames
    new_user.phone_number = new_user_data.phone_number
    new_user.age = new_user_data.age
    new_user.birthday = new_user_data.birthday
    return new_user

async def get_user_by_email(
    db: AsyncSession,
    email: str
):
    stmt = select(User).where(User.email == email)
    user = await db.execute(stmt)

    user = user.scalar_one_or_none()

    if not user:
        return None

    stmt = select(UserData).where(UserData.user_id == user.id)
    user_data = await db.execute(stmt)

    user_data = user_data.scalar_one_or_none()

    user.names = user_data.names
    user.lastnames = user_data.lastnames
    user.phone_number = user_data.phone_number
    user.age = user_data.age
    user.birthday = user_data.birthday

    return user

async def get_user_by_id(
    db: AsyncSession,
    user_id: int
):
    stmt = select(User).where(User.id == user_id)
    user = await db.execute(stmt)

    user = user.scalar_one_or_none()

    if not user:
        return None

    stmt = select(UserData).where(UserData.user_id == user.id)
    user_data = await db.execute(stmt)

    user_data = user_data.scalar_one_or_none()

    user.names = user_data.names
    user.lastnames = user_data.lastnames
    user.phone_number = user_data.phone_number
    user.age = user_data.age
    user.birthday = user_data.birthday

    return user


