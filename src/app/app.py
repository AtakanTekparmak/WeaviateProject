from fastapi import FastAPI
from app import models
from app.crud_router import create_crud_router
from app.database import create_tables

# Instantiate the FastAPI app
app = FastAPI()

# Create tables 
create_tables()

car_router = create_crud_router(
    model=models.Car,
    create_schema=models.CarCreate,
    update_schema=models.CarUpdate,
    response_schema=models.CarResponse,
)

driver_router = create_crud_router(
    model=models.Driver,
    create_schema=models.DriverCreate,
    update_schema=models.DriverUpdate,
    response_schema=models.DriverResponse,
)

app.include_router(car_router, prefix="/cars", tags=["cars"])
app.include_router(driver_router, prefix="/drivers", tags=["drivers"])