from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(description="Unique username for the new account", json_schema_extra={"example":"johndoe"})
    email: EmailStr = Field(description="Valid email address", json_schema_extra={"example":"john@example.com"})
    password: str = Field(description="Password (will be hashed before storage)", json_schema_extra={"example":"Str0ng!Pass"})

class UserLogin(BaseModel):
    username: str = Field(description="Your username", json_schema_extra={"example":"johndoe"})
    email: EmailStr = Field(description="Your registered email", json_schema_extra={"example":"john@example.com"})
    password: str = Field(description="Your password", json_schema_extra={"example":"Str0ng!Pass"})

class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(description="Token type (always 'bearer')", json_schema_extra={"example":"bearer"})
