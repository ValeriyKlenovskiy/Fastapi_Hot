from typing import List

from pydantic import BaseModel, ConfigDict


class HotelsSchema(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class HotelsInfoSchema(HotelsSchema):
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
