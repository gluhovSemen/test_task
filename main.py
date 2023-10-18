from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from config import Settings
from db import get_session
from schemas import UserCreate
from services import (create_user, create_user_token, get_user_by_email,
                      get_user_by_token)
from utils import get_signature

app = FastAPI()


@app.post("/sign_up")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_db = await get_user_by_email(session, user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(session, user)
    signature = get_signature(user.id, Settings.PRIVATE_KEY)
    return {"user_id": user.id, "signature": signature}


@app.post("/sign_in", response_model=dict)
async def sign_in_user(
    sign_in_data: schemas.UserSignIn, session: AsyncSession = Depends(get_session)
):
    user_db = await get_user_by_email(session, sign_in_data.email)
    if not user_db or sign_in_data.password != user_db.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    auth_token = await create_user_token(session, user_db)
    return {"auth_token": auth_token}


@app.get("/user", response_model=dict)
async def get_user(auth_token: str, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_token(session, auth_token)
    return {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "eth_address": user.eth_address,
    }
