from pydantic import BaseModel, EmailStr
from datetime import date

class SignupRequest(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    dob: date
    salary: float

class SignupResponse(BaseModel):
    message: str
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    username: str
    token: str