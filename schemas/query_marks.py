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
    query = {}
    if self.habit:
      query['habit_id'] = self.habit

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
          'times': 1,
          'note': 1
      }})

    return pipeline


"""
[
  {
    $addFields: {
      habit_id: {
        $toObjectId: "$habit_id"
      }
    }
  },
  {
    $lookup: {
      from: "habits",
      localField: "habit_id",
      foreignField: "_id",
      as: "habit"
    }
  },
  {
    $unwind: "$habit"
  },
  {
    $match: {
      "habit.user_id": "67bac0a2afe5a7b1ca9508c8"
    }
  },
  {
    $group: {
      _id: "$date",
      marks: {
        $push: {
          times: "$times",
          habit_name: "$habit.name",
          habit_emoji: "$habit.emoji"
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      date: "$_id",
      marks: 1
    }
  }
]"""
