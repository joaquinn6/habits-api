from repositories.mark_repository import MarkRepository
from schemas.query_stats import StatsQuery


class StatsService():
  def __init__(self) -> None:
    self._repo_marks = MarkRepository()

  def get_stats(self, query: StatsQuery) -> dict:
    pipelines = query.get_pipelines()
    data = {}
    for pipeline in pipelines:
      data[pipeline['name']] = list(
          self._repo_marks.aggregate(pipeline['pipeline']))
    return data
