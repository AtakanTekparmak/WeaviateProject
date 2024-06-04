from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from datetime import datetime

from app.database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)

    drivers = relationship("Driver", back_populates="car")

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
        }

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    license_number = Column(String, unique=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))

    car = relationship("Car", back_populates="drivers")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "license_number": self.license_number,
            "car_id": self.car_id,
        }
    
class MaintenanceReport(Base):
    __tablename__ = "maintenance_reports"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    date = Column(DateTime)
    time = Column(DateTime)
    report = Column(String)
    price_paid = Column(Float)

    car = relationship("Car", backref="maintenance_reports")

    def to_dict(self):
        return {
            "id": self.id,
            "car_id": self.car_id,
            "date": self.date,
            "time": self.time,
            "report": self.report,
            "price_paid": self.price_paid,
        }

class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    insurer = Column(String)
    begin_date = Column(DateTime)
    end_date = Column(DateTime)
    price_paid = Column(Float)

    car = relationship("Car", backref="insurances")
    driver = relationship("Driver", backref="insurances")

    def to_dict(self):
        return {
            "id": self.id,
            "car_id": self.car_id,
            "driver_id": self.driver_id,
            "insurer": self.insurer,
            "begin_date": self.begin_date,
            "end_date": self.end_date,
            "price_paid": self.price_paid,
        }

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
        from_attributes = True

class MaintenanceReportBase(BaseModel):
    car_id: int
    date: datetime
    time: datetime
    report: str
    price_paid: float

class MaintenanceReportCreate(MaintenanceReportBase):
    pass

class MaintenanceReportUpdate(MaintenanceReportBase):
    pass

class MaintenanceReportResponse(MaintenanceReportBase):
    id: int

    class Config:
        from_attributes = True

class InsuranceBase(BaseModel):
    car_id: int
    driver_id: int
    insurer: str
    begin_date: datetime
    end_date: datetime
    price_paid: float

class InsuranceCreate(InsuranceBase):
    pass

class InsuranceUpdate(InsuranceBase):
    pass

class InsuranceResponse(InsuranceBase):
    id: int

    class Config:
        from_attributes = True