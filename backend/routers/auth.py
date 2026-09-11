from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    AuthResponse
)

from security import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=201
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email is already registered."
        )


    # Check username
    existing_username = (
        db.query(User)
        .filter(
            User.username == request.username
        )
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username is already taken."
        )


    # Hash password
    hashed_password = hash_password(
        request.password
    )


    # Create user
    user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return {
        "success": True,
        "message": "Account created successfully.",
        "access_token": None,
        "token_type": None
    }


# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=AuthResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find user
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )


    # Check user and password
    if (
        not user
        or not verify_password(
            request.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    # Create JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        },
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    return {
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer"
    }