import re
from bson import ObjectId
from models.habit_model import Habit
from repositories.habit_repository import HabitRepository
from schemas.habit_schema import (HabitCreateResponse, HabitCreate, HabitQuery)


class HabitService():
  def __init__(self) -> None:
    self._repo = HabitRepository()

  def create_habit(self, habit: Habit) -> HabitCreateResponse:
    habit.new()
    self._repo.insert(habit)
    return habit

  def update_habit(self, entity: Habit, habit: Habit) -> Habit:
    entity.update(habit)
    self._repo.update_by_id(entity)
    return entity

  def get_query(self, query_params: HabitQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _create_entity(self, habit: HabitCreate) -> dict:
    return {
        '_id': ObjectId(),
        'name': habit.name.capitalize(),
        'code': habit.code.upper(),
        'categories': habit.categories,
        'description': habit.description.capitalize(),
        'purchase_price': 0.0,
        'sale_price': 0.0,
        'stock': 0
    }

  def _update_entity(self, habit: HabitCreate) -> dict:
    return {
        'name': habit.name.capitalize(),
        'code': habit.code.upper(),
        'categories': habit.categories,
        'description': habit.description.capitalize(),
    }

  def _get_query(self, query_params: HabitQuery) -> dict:
    query = dict({})

    if query_params.name:
      query['name'] = re.compile(f'.*{query_params.name}.*', re.I)

    if query_params.code:
      query['code'] = re.compile(f'{query_params.code.upper()}.*', re.I)
    if query_params.categories:
      query['categories'] = {'$in': query_params.categories}
    if query_params.in_stock is not None:
      if not query_params.in_stock:
        query['stock'] = 0
      else:
        query['stock'] = {'$gt': 0}
    return query

  def _get_pagination(self, query_params: HabitQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }
