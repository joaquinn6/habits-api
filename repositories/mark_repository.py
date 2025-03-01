from models.mark_model import Mark
from repositories.repository import RepositoryBase


class MarkRepository(RepositoryBase[Mark]):

  def __init__(self) -> None:
    super().__init__('marks', Mark.from_dict)
