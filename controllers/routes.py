"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller, habit_controller, mark_controller
router = APIRouter()
router.include_router(users_controller.router)
router.include_router(habit_controller.router)
router.include_router(mark_controller.router)
