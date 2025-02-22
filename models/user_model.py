from datetime import datetime
from pydantic import Field

from models.entity import Entity


class User(Entity):
  email: str = Field(...,
                     pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
  first_name: str = Field(...)
  last_name: str = Field(default="")
  birth_date: datetime = Field(...)
  password: str = Field(...)

  def new(self):
    self.initialize()

  def update(self, new_item: "User"):
    self.on_update()
    self.first_name = new_item.first_name
    self.last_name = new_item.last_name
    self.birth_date = new_item.birth_date

  def change_password(self, new_password: str):
    self.on_update()
    self.password = new_password
