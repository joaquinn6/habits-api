from datetime import datetime
from enum import Enum
from pydantic import Field

from models.entity import Entity


class Genders(str, Enum):
  FEMALE = "FEMALE"
  MALE = "MALE"


class User(Entity):
  email: str = Field(...,
                     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", max_length=80)
  first_name: str = Field(..., max_length=40)
  last_name: str = Field(default="", max_length=40)
  country: str = Field(default="", max_length=2)
  gender: Genders = Field(default="")
  birth_date: datetime = Field(...)
  password: str = Field(...)

  def new(self):
    self.initialize()

  def update(self, new_item: "User"):
    self.on_update()
    self.first_name = new_item.first_name
    self.last_name = new_item.last_name
    self.country = new_item.country
    self.gender = new_item.gender
    self.birth_date = new_item.birth_date

  def change_password(self, new_password: str):
    self.on_update()
    self.password = new_password
