from enum import Enum
from pydantic import BaseModel, Field

from models.entity import Entity


class TypeHabit(str, Enum):
  bad = "BAD"
  good = "GOOD"


class GoalHabit(BaseModel):
  per_day: int = Field(...)
  per_week: int = Field(...)
  per_month: int = Field(...)
  per_year: int = Field(...)


class Habit(Entity):
  name: str = Field(...)
  description: str = Field(default="")
  type: TypeHabit = Field(...)
  goal: GoalHabit = Field(...)
  user_id: str = Field(default=None)
  color: str = Field(default="")

  def new(self):
    self.initialize()

  def update(self, new_item: "Habit"):
    self.on_update()
    self.name = new_item.name
    self.description = new_item.description
    self.type = new_item.type
    self.goal = new_item.goal
    self.color = new_item.color
