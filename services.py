from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthToken, User
from schemas import UserCreate
from utils import create_auth_token


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        eth_address=user.eth_address,
        password=user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_token(db: AsyncSession, user: User) -> AuthToken.token:
    db_token = AuthToken(user_id=user.id, token=create_auth_token())
    db.add(db_token)
    await db.commit()
    return db_token.token


async def get_user_by_token(db: AsyncSession, token: str) -> User:
    statement = select(AuthToken).where(AuthToken.token == token)
    result = await db.execute(statement)
    try:
        user_id = result.scalars().first().user_id
        statement = select(User).where(User.id == user_id)
        result = await db.execute(statement)
        return result.scalars().first()
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid token")
