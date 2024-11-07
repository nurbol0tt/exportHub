from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str



class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenRequest(BaseModel):
    token: str


class UserProfileResponse(BaseModel):
    username: str
    email: str
