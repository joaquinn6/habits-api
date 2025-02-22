from models.habit_model import Habit
from repositories.repository import RepositoryBase


class HabitRepository(RepositoryBase[Habit]):

  def __init__(self) -> None:
    super().__init__('habits', Habit.from_dict)
