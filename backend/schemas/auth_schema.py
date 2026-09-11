from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


class AuthResponse(BaseModel):

    success: bool

    message: str

    access_token: str | None = None

    token_type: str | None = None