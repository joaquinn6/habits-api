"""Routes y controllers de marks"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from models.mark_model import Mark
from services.mark_service import MarkService
from repositories.mark_repository import MarkRepository
AUTH_SCHEME = OptionalHTTPBearer()
REPO = MarkRepository()
SERVICE = MarkService()

router = APIRouter(
    prefix="",
    tags=["Marks"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/habits/{habit_id}/marks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new mark"
)
async def create(
        habit_id: str,
        token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME),
        mark: Mark = Body(...)) -> str:
  AuthService().is_logged(token)
  mark.habit_id = habit_id
  mark = SERVICE.create_mark(mark)
  return str(mark.id)


@router.get(
    "/marks/{mark_id}",
    status_code=status.HTTP_200_OK,
    summary="Get mark by id"
)
async def get_by_id(mark_id: str, token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> Mark:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(mark_id)
  if not entity:
    helpers_api.raise_error_404('Marko')
  return entity.model_dump(by_alias=True)


@router.put(
    "/marks/{mark_id}",
    status_code=status.HTTP_200_OK,
    summary="Update mark by id"
)
async def mark_update_by_id(
        mark_id: str,
        mark: Mark = Body(...),
        token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> str:
  AuthService().is_logged(token)
  entity = REPO.get_by_id(mark_id)
  if not entity:
    helpers_api.raise_error_404('Mark')
  update_mark = SERVICE.update_mark(entity, mark)
  return str(update_mark.id)

# TODO> los gets de las marcas como se debe


@router.get(
    "/habits/{habit_id}/marks",
    status_code=status.HTTP_200_OK,
    summary="Get marks"
)
async def get_marks_by_habit(token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> list[Mark]:
  data = AuthService().get_content_token(token)
  AuthService().is_logged(token)
  marks = SERVICE.get_marks_by_habit(data['id'])
  return [mark.model_dump(by_alias=True) for mark in marks]


@router.get(
    "/marks",
    status_code=status.HTTP_200_OK,
    summary="Get marks"
)
async def get_marks(token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME)) -> list[Mark]:
  data = AuthService().get_content_token(token)
  AuthService().is_logged(token)
  marks = SERVICE.get_marks_by_habit(data['id'])
  return [mark.model_dump(by_alias=True) for mark in marks]
