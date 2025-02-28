"""Routes y controllers de habitos"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import TypeAdapter
from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from models.habit_model import Habit
from services.habit_service import HabitService
from repositories.habit_repository import HabitRepository
AUTH_SCHEME = OptionalHTTPBearer()
REPO = HabitRepository()
SERVICE = HabitService()

router = APIRouter(
    prefix="",
    tags=["Habits"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/habits",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new habit"
)
async def create(token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME), habit: Habit = Body(...)) -> str:
  data = AuthService().get_content_token(token)
  habit.user_id = data['id']
  habit = SERVICE.create_habit(habit)
  return str(habit.id)


@router.get(
    "/habits/{habit_id}",
    status_code=status.HTTP_200_OK,
    summary="Get habit by id"
)
async def get_by_id(habit_id: str, token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> Habit:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(habit_id)
  if not entity:
    helpers_api.raise_error_404('Habito')
  return entity.model_dump(by_alias=True)


@router.put(
    "/habits/{habit_id}",
    status_code=status.HTTP_200_OK,
    summary="Update habit by id"
)
async def habit_update_by_id(
        habit_id: str,
        habit: Habit = Body(...),
        token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> str:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(habit_id)
  if not entity:
    helpers_api.raise_error_404('Habit')
  update_habit = SERVICE.update_habit(entity, habit)
  return str(update_habit.id)


@router.get(
    "/habits",
    status_code=status.HTTP_200_OK,
    summary="Get habits"
)
async def get_habits(token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> list[Habit]:
  data = AuthService().get_content_token(token)
  AuthService().is_logged(token)
  habits = SERVICE.get_habits_by_user(data['id'])
  return [habit.model_dump(by_alias=True) for habit in habits]
