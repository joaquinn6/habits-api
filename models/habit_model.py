from enum import Enum
from pydantic import BaseModel, Field

from models.entity import Entity


class TypeHabit(str, Enum):
  BAD = "BAD"
  GOOD = "GOOD"


class GoalHabit(BaseModel):
  times: int = Field(...)
  measure: str = Field(...)
  per_week: int = Field(...)
  per_month: int = Field(...)
  per_year: int = Field(...)


class Habit(Entity):
  name: str = Field(...)
  description: str = Field(default="")
  type: TypeHabit = Field(...)
  with_goals: bool
  goals: GoalHabit | None = Field(default=None)
  user_id: str = Field(default=None)
  color: str = Field(default="")
  emoji: str = Field(default="")

  def new(self):
    self.initialize()

  def update(self, new_item: "Habit"):
    self.on_update()
    self.name = new_item.name
    self.description = new_item.description
    self.type = new_item.type
    self.goals = new_item.goals
    self.with_goals = new_item.with_goals
    self.color = new_item.color
    self.emoji = new_item.emoji
