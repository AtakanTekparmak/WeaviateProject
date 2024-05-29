from fastapi import FastAPI, Depends
from . import models, crud

app = FastAPI()

# Dependency
def get_db():
    db = []
    return db

# Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/", response_model=models.Item)
async def create_item(item: models.ItemCreate, db=Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items/", response_model=list[models.Item])
async def read_items(db=Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=models.Item)
async def read_item(item_id: int, db=Depends(get_db)):
    return crud.get_item(db, item_id)

@app.put("/items/{item_id}", response_model=models.Item)
async def update_item(item_id: int, item: models.ItemUpdate, db=Depends(get_db)):
    return crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db=Depends(get_db)):
    return crud.delete_item(db, item_id)