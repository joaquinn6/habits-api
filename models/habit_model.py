from enum import Enum
from pydantic import BaseModel, Field

from models.entity import Entity


class TypeHabit(str, Enum):
  BAD = "BAD"
  GOOD = "GOOD"


class TypeMeasures(str, Enum):
  MONTH = "MONTH"
  WEEK = "WEEK"
  YEAR = "YEAR"


class GoalHabit(BaseModel):
  times: int = Field(...)
  measure: TypeMeasures = Field(...)
  per_week: int = Field(...)
  per_month: int = Field(...)
  per_year: int = Field(...)


class Habit(Entity):
  name: str = Field(..., max_length=20)
  description: str = Field(default="", max_length=40)
  type: TypeHabit = Field(...)
  with_goals: bool
  goals: GoalHabit | None = Field(default=None)
  user_id: str = Field(default=None)
  color: str = Field(default="")
  emoji: str = Field(default="", max_length=7)

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
