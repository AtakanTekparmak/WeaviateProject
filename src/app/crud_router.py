from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_crud_router(model, create_schema, update_schema, response_schema):
    router = APIRouter()

    @router.post("/", response_model=response_schema)
    def create(item: create_schema, db: Session = Depends(get_db)):
        db_item = model(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.get("/", response_model=list[response_schema])
    def read_all(db: Session = Depends(get_db)):
        items = db.query(model).all()
        return items

    @router.get("/{item_id}", response_model=response_schema)
    def read(item_id: int, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    @router.put("/{item_id}", response_model=response_schema)
    def update(item_id: int, item: update_schema, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        for field, value in item.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.delete("/{item_id}")
    def delete(item_id: int, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"message": f"Item {item_id} deleted successfully"}

    return router