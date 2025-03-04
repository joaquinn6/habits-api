from models.mark_model import Mark
from repositories.mark_repository import MarkRepository


class MarkService():
  def __init__(self) -> None:
    self._repo = MarkRepository()

  def create_mark(self, mark: Mark) -> Mark:
    mark.new()
    self._repo.insert(mark)
    return mark

  def update_mark(self, entity: Mark, mark: Mark) -> Mark:
    entity.update(mark)
    self._repo.update_by_id(entity)
    return entity
