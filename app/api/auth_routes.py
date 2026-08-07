from fastapi import APIRouter, HTTPException

from app.db.mongodb import database
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(register_request: RegisterRequest):

    existing_user = await database.users.find_one(
        {"email": register_request.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = {
        "full_name": register_request.full_name,
        "email": register_request.email,
        "hashed_password": hash_password(register_request.password)
    }

    await database.users.insert_one(new_user)

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
async def login_user(login_request: LoginRequest):

    existing_user = await database.users.find_one(
        {"email": login_request.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_matches = verify_password(
        login_request.password,
        existing_user["hashed_password"]
    )

    if not password_matches:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(existing_user["email"])

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }