from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from schemas.query_stats import StatsQuery
from repositories.mark_repository import MarkRepository
from services.stats_service import StatsService
AUTH_SCHEME = OptionalHTTPBearer()
REPO = MarkRepository()
SERVICE = StatsService()

router = APIRouter(
    prefix="",
    tags=["Stats"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/habits/{habit_id}/stats",
    status_code=status.HTTP_200_OK,
    summary="get stats by habit"
)
async def get_stats(
        habit_id: str,
        token: HTTPAuthorizationCredentials = Depends(AUTH_SCHEME),
        query_params: StatsQuery = Query(...),) -> dict:
  AuthService().is_logged(token)
  query_params.habit = habit_id
  stats = SERVICE.get_stats(query_params)
  return stats
