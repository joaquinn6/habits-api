from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class TypeStats(str, Enum):
  NONE = "NONE"
  MONTH = "MONTH"
  WEEK = "WEEK"


class StatsQuery(BaseModel):
  habit: str = Field(default='')
  type: TypeStats = Field(default=TypeStats.NONE.value)
  week: int = Field(default=0)
  month: int = Field(default=0)
  year: int = Field(default=0)
  start_date: datetime = Field(
      default=datetime(datetime.now().year, 1, 1, 0, 0, 0))

  @property
  def end_date(self):
    return datetime(datetime.now().year + 1, 1, 1, 0, 0, 0)

  def get_pipelines(self) -> list:
    match (self.type):
      case TypeStats.NONE.value:
        return self.pipelines_by_none()
      case TypeStats.WEEK.value:
        return self.pipelines_by_week()
      case TypeStats.MONTH.value:
        return self.pipelines_by_month()

  def pipelines_by_none(self) -> List:
    return [
        {"name": "totalByYear", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$group": {"_id": "$habit_id", "total_times": {"$sum": "$times"}}},
            {"$project": {"total_times": 1, "_id": 0}}
        ]},
        {"name": "bestLastDay", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$sort": {"times": -1, "date": -1}},
            {"$group": {"_id": "$habit_id", "best_day": {"$first": "$$ROOT"}}},
            {"$replaceRoot": {"newRoot": "$best_day"}},
            {"$project": {"_id": 0}}
        ]},
        {"name": "bestWeek", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$group": {"_id": {"$week": "$date"},
                        "total_times": {"$sum": "$times"}}},
            {"$sort": {"total_times": -1, "_id": -1}},
            {"$limit": 1},
            {"$project": {"_id": 0, "week": "$_id", "total_times": 1}}
        ]},
        {"name": "bestMonth", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$group": {"_id": {"$month": "$date"},
                        "total_times": {"$sum": "$times"}}},
            {"$sort": {"total_times": -1, "_id": -1}},
            {"$limit": 1},
            {"$project": {"_id": 0, "month": "$_id", "total_times": 1}}
        ]}
    ]

  def pipelines_by_week(self) -> List:
    pipelines = self.pipelines_by_none()
    pipelines.append({
        "name": "groupByWeek", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$group": {"_id": {"year": {"$year": "$date"}, "week": {
                "$isoWeek": "$date"}}, "total_times": {"$sum": "$times"}}},
            {"$project": {"week": "$_id.week", "total_times": 1, "_id": 0}}
        ]
    })
    return pipelines

  def pipelines_by_month(self) -> List:
    pipelines = self.pipelines_by_none()
    pipelines.append({
        "name": "groupByMonth", "pipeline": [
            {"$match": {"habit_id": self.habit, "date": {
                "$gte": self.start_date, "$lt": self.end_date}}},
            {"$group": {"_id": {"$month": "$date"},
                        "total_times": {"$sum": "$times"}}},
            {"$sort": {"_id": 1}}
        ]
    })
    return pipelines
