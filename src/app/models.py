from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from app.database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)

    drivers = relationship("Driver", back_populates="car")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    license_number = Column(String, unique=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))

    car = relationship("Car", back_populates="drivers")

class CarBase(BaseModel):
    make: str
    model: str
    year: int

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

    class Config:
        from_attributes = True

class DriverBase(BaseModel):
    name: str
    license_number: str

class DriverCreate(DriverBase):
    car_id: int

class DriverUpdate(DriverBase):
    car_id: int | None = None

class DriverResponse(DriverBase):
    id: int
    car_id: int

    class Config:
        ofrom_attributes = True