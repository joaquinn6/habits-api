from pydantic import BaseModel, Field


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)


class UserChangePassword(BaseModel):
  new_password: str = Field(...)
  old_password: str = Field(...)
