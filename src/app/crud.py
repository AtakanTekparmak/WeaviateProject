from . import models

# In-memory database
db = []
item_id = 0

def create_item(db: list, item: models.ItemCreate):
    global item_id
    item_id += 1
    new_item = models.Item(id=item_id, **item.dict())
    db.append(new_item)
    return new_item

def get_items(db: list):
    return db

def get_item(db: list, item_id: int):
    for item in db:
        if item.id == item_id:
            return item
    return None

def update_item(db: list, item_id: int, item: models.ItemUpdate):
    for i, db_item in enumerate(db):
        if db_item.id == item_id:
            updated_item = item.dict(exclude_unset=True)
            db_item = db_item.copy(update=updated_item)
            db[i] = db_item
            return db_item
    return None

def delete_item(db: list, item_id: int):
    for i, item in enumerate(db):
        if item.id == item_id:
            del db[i]
            return {"message": f"Item {item_id} deleted successfully"}
    return {"message": f"Item {item_id} not found"}