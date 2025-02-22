from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Token(BaseModel):
  token: str = Field(...)
  email: str = Field(...)
  id: str = Field(...)

  @field_validator("id", mode="before")
  @classmethod
  def convert_id_to_str(cls, value):
    if isinstance(value, ObjectId):
      return str(value)
    return value

  def dict(self, *args, **kwargs):
    original_dict = super().model_dump(*args, **kwargs)
    if original_dict.get("id"):
      original_dict["id"] = ObjectId(original_dict["id"])
    return original_dict
