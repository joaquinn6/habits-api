"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from models.user_model import User
from models.token_model import Token
from schemas.user_schema import (UserLogin, UserChangePassword)
from services.user_service import UserService
from repositories.user_repository import UserRepository

AUTH_SCHEME = OptionalHTTPBearer()
REPO = UserRepository()
SERVICE = UserService()

router = APIRouter(
    prefix="",
    tags=["Usuario"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users/{user_id}/password",
    status_code=status.HTTP_200_OK,
    summary="Change password"
)
async def change_password(user_id: str, token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME), user: UserChangePassword = Body(...)):
  AuthService().is_logged(token)

  entity = REPO.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('User')
  SERVICE.change_password(user, entity)
  return


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create(user: User = Body(...)) -> str:
  new_user = SERVICE.create_user(user)
  return str(new_user.id)


@router.delete(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Delete a user"
)
async def delete(token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> str:
  data = AuthService().get_content_token(token)
  SERVICE.delete_user(data['id'])
  return data['id']


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by id"
)
async def get_by_id(user_id: str, token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> User:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('User')
  return entity.model_dump(by_alias=True)


@router.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user by id"
)
async def user_update_by_id(
        user_id: str,
        user: User = Body(...),
        token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> str:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('User')
  update_user = SERVICE.update_user(entity, user)
  return str(update_user.id)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(user: UserLogin = Body(...)) -> Token:
  token = AuthService().generate_token(user.email, user.password)
  return token
