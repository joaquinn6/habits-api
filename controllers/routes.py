"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller
from controllers import habits_controller
router = APIRouter()
router.include_router(users_controller.router)
router.include_router(habits_controller.router)
