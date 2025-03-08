from pydantic import BaseModel, Field
from enum import Enum

from core.utils import range_of_date


class TypeHabit(str, Enum):
  YEAR = "YEAR"
  MONTH = "MONTH"


class MarkQuery(BaseModel):
  type: TypeHabit = Field(default=None)
  month: int = Field(default=0)
  year: int = Field(default=0)

  def to_pipeline(self, habit: str = None):
    query = {}
    if habit:
      query['habit_id'] = habit

    if self.type:
      fist_date, end_date = range_of_date(self.year, self.month)
      query['date'] = {'$gte': fist_date, '$lte': end_date}

    pipeline = [
        {
            '$match': query
        }
    ]

    if self.type == TypeHabit.YEAR:
      pipeline.append({'$group': {
          '_id': {
              'year': {
                  '$year': "$date"
              },
              'month': {
                  '$month': "$date"
              }
          },
          'times': {
              '$sum': "$times"
          }
      }})
      pipeline.append({'$project': {
          '_id': 0,
          'year': "$_id.year",
          'month': "$_id.month",
          'times': 1
      }})
    else:
      pipeline.append({'$project': {
          '_id': {'$toString': '$_id'},
          'date': 1,
          'times': 1
      }})

    return pipeline
