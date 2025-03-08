from typing import List
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
  user: str = Field(default='')
  habit: str = Field(default='')

  def to_pipeline(self):
    if self.habit:
      return self.pipeline_by_habit()
    return self.pipeline_by_user()

  def pipeline_by_habit(self) -> List:
    query = {'habit_id': self.habit}

    first_date, end_date = range_of_date(self.year, self.month)
    query['date'] = {'$gte': first_date, '$lte': end_date}

    pipeline = [
        {
            '$match': query
        }
    ]

    if self.type == TypeHabit.YEAR.value:
      pipeline.append({'$group': {
          '_id': {
              'year': {
                  '$year': "$date"
              },
              'month': {
                  '$month': "$date"
              },
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
          'times': 1,
          'note': 1
      }})

    return pipeline

  def pipeline_by_user(self) -> List:
    first_date, end_date = range_of_date(self.year, self.month)
    if self.type == TypeHabit.YEAR:
      return self.pipeline_by_user_year(first_date, end_date)
    return self.pipeline_by_user_month(first_date, end_date)

  def pipeline_by_user_month(self, first_date, end_date) -> List:
    return [
        {
            '$match': {'date': {'$gte': first_date, '$lte': end_date}}
        },
        {
            '$addFields': {
                'habit_id': {
                    '$toObjectId': "$habit_id"
                }
            }
        },
        {
            '$lookup': {
                'from': "habits",
                'localField': "habit_id",
                'foreignField': "_id",
                'as': "habit"
            }
        },
        {
            '$unwind': "$habit"
        },
        {
            '$match': {
                "habit.user_id": self.user

            }
        },
        {
            '$group': {
                '_id': "$date",
                'marks': {
                    '$push': {
                        'times': "$times",
                        'habit_name': "$habit.name",
                        'habit_emoji': "$habit.emoji"
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'date': "$_id",
                'marks': 1
            }
        }
    ]

  def pipeline_by_user_year(self, first_date, end_date) -> List:
    return [
        {
            '$match': {'date': {'$gte': first_date, '$lte': end_date}}
        },
        {
            '$addFields': {
                'habit_id': {
                    '$toObjectId': "$habit_id"
                }
            }
        },
        {
            '$lookup': {
                'from': "habits",
                'localField': "habit_id",
                'foreignField': "_id",
                'as': "habit"
            }
        },
        {
            '$unwind': "$habit"
        },
        {
            '$match': {
                "habit.user_id": self.user
            }
        },
        {
            '$group':
            {
                '_id': {
                    'year': {'$year': "$date"},
                    'month': {'$month': "$date"},
                    "habit_id": "$habit._id"
                },
                "times": {"$sum": "$times"},
                "habit_name": {"$first": "$habit.name"},
                "habit_emoji": {"$first": "$habit.emoji"}
            }},
        {
            "$group": {
                "_id": {"year": "$_id.year", "month": "$_id.month"},
                "marks": {
                    "$push": {
                        "times": "$times",
                        "habit_name": "$habit_name",
                        "habit_emoji": "$habit_emoji"
                    }
                }
            }
        },
        {

                "$project": {
                    "_id": 0,
                    "year": "$_id.year",
                    "month": "$_id.month",
                    "marks": 1
                }
        },
    ]
