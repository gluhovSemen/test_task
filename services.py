from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthToken, User
from schemas import UserCreate
from utils import create_auth_token


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        eth_address=user.eth_address,
        password=user.password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def create_user_token(session: AsyncSession, user: User) -> AuthToken.token:
    db_token = AuthToken(user_id=user.id, token=create_auth_token())
    session.add(db_token)
    await session.commit()
    return db_token.token


async def get_user_by_token(session: AsyncSession, token: str) -> User:
    statement = select(AuthToken).where(AuthToken.token == token)
    result = await session.execute(statement)
    try:
        user_id = result.scalars().first().user_id
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        return result.scalars().first()
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid token")
