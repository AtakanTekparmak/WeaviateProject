from pydantic import BaseModel

class SubItem(BaseModel):
    name: str
    description: str

class ItemBase(BaseModel):
    name: str
    price: float

class ItemCreate(ItemBase):
    sub_item: SubItem

class ItemUpdate(ItemBase):
    sub_item: SubItem | None = None

class Item(ItemBase):
    id: int
    sub_item: SubItem

    class Config:
        from_attributes = True