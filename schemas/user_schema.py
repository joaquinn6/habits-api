from pydantic import BaseModel, Field


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)


class UserChangePassword(BaseModel):
  email: str = Field(...)
  password: str = Field(...)
  oldPassword: str = Field(...)
