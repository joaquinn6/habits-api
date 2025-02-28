from models.habit_model import Habit
from repositories.habit_repository import HabitRepository


class HabitService():
  def __init__(self) -> None:
    self._repo = HabitRepository()

  def create_habit(self, habit: Habit) -> Habit:
    habit.new()
    self._repo.insert(habit)
    return habit

  def update_habit(self, entity: Habit, habit: Habit) -> Habit:
    entity.update(habit)
    self._repo.update_by_id(entity)
    return entity

  def get_habits_by_user(self, id_user: str) -> list[Habit]:
    query = {
        'user_id': id_user
    }
    return self._repo.get(query)
