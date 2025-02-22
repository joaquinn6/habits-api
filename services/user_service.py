from core import helpers_api
from core.auth import AuthService
from models.user_model import User
from schemas.user_schema import UserChangePassword
from repositories.user_repository import UserRepository


class UserService():
  def __init__(self) -> None:
    self._repo = UserRepository()
    self._auth_service = AuthService()

  def create_user(self, user: User) -> User:
    if self._repo.exist_by_email(user.email):
      helpers_api.raise_error_409('Email')
    user.password = self._auth_service.get_password_hash(user.password)
    user.new()
    self._repo.insert(user)
    return user

  def update_user(self, entity: User, user: User) -> User:
    entity.update(user)
    self._repo.update_by_id(entity)
    return entity

  def change_password(self, req_password: UserChangePassword, user: User):
    if not self._auth_service.verify_password(req_password.oldPassword, user.password):
      helpers_api.raise_error_422()

    new_hashed_password = self._auth_service.get_password_hash(
        req_password.password)
    user.change_password(new_hashed_password)
    self._repo.update_by_id(user)
    return
