from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(description="Unique username for the new account", example="johndoe")
    email: EmailStr = Field(description="Valid email address", example="john@example.com")
    password: str = Field(description="Password (will be hashed before storage)", example="Str0ng!Pass")

class UserLogin(BaseModel):
    username: str = Field(description="Your username", example="johndoe")
    email: EmailStr = Field(description="Your registered email", example="john@example.com")
    password: str = Field(description="Your password", example="Str0ng!Pass")

class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(description="Token type (always 'bearer')", example="bearer")
