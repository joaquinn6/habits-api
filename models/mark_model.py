from datetime import datetime
from pydantic import Field

from models.entity import Entity


class Mark(Entity):
  date: datetime = Field(...)
  times: int = Field(default=1)
  habit_id: str = Field(default="")
  note: str = Field(default="")

  def new(self):
    self.initialize()

  def update(self, new_item: "Mark"):
    self.on_update()
    self.times = new_item.times
    self.note = new_item.note
