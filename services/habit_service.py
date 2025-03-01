from models.habit_model import Habit
from repositories.habit_repository import HabitRepository
from repositories.mark_repository import MarkRepository


class HabitService():
  def __init__(self) -> None:
    self._repo = HabitRepository()
    self._repo_marks = MarkRepository()

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

  def delete_habit(self, id_habit: str):
    self._repo.delete_by_id(id_habit)
    query = {
        'habit_id': id_habit
    }
    self._repo_marks.delete_many(query)
    return
