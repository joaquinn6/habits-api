from core import helpers_api
from core.auth import AuthService
from models.user_model import User
from schemas.user_schema import UserChangePassword
from repositories.user_repository import UserRepository
from services.habit_service import HabitService


class UserService():
  def __init__(self) -> None:
    self._repo = UserRepository()
    self._habit_service = HabitService()
    self._auth_service = AuthService()

  def create_user(self, user: User) -> User:
    if self._repo.exist_by_email(user.email):
      helpers_api.raise_error_409('Email')
    user.password = self._auth_service.get_password_hash(user.password)
    user.new()
    self._repo.insert(user)
    return user

  def delete_user(self, id_user: str):
    habits = self._habit_service.get_habits_by_user(id_user)
    for habit in habits:
      self._habit_service.delete_habit(habit.id)
    self._repo.delete_by_id(id_user)

  def update_user(self, entity: User, user: User) -> User:
    entity.update(user)
    self._repo.update_by_id(entity)
    return entity

  def change_password(self, req_password: UserChangePassword, user: User):
    if not self._auth_service.verify_password(req_password.old_password, user.password):
      helpers_api.raise_error_422()

    new_hashed_password = self._auth_service.get_password_hash(
        req_password.new_password)
    user.change_password(new_hashed_password)
    self._repo.update_by_id(user)
    return
