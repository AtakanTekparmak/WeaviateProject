from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import models
from app.crud_router import create_crud_router
from app.database import create_tables

# Instantiate the FastAPI app
app = FastAPI()

# Create tables 
create_tables()

# Create CRUD routers
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

maintenance_report_router = create_crud_router(
    model=models.MaintenanceReport,
    create_schema=models.MaintenanceReportCreate,
    update_schema=models.MaintenanceReportUpdate,
    response_schema=models.MaintenanceReportResponse,
)

insurance_router = create_crud_router(
    model=models.Insurance,
    create_schema=models.InsuranceCreate,
    update_schema=models.InsuranceUpdate,
    response_schema=models.InsuranceResponse,
)

# Include the routers
app.include_router(car_router, prefix="/cars", tags=["cars"])
app.include_router(driver_router, prefix="/drivers", tags=["drivers"])
app.include_router(maintenance_report_router, prefix="/maintenance_reports", tags=["maintenance_reports"])
app.include_router(insurance_router, prefix="/insurances", tags=["insurances"])

# Create a route to get the OpenAPI schema
@app.get("/docs_info")
def get_docs_info():
    """ Get the OpenAPI schema """
    # Get the OpenAPI schema
    openapi_schema = get_openapi(
        title="App Title",
        version="1.0.0",
        description="App Description",
        routes=app.routes,
    )
    schemas = openapi_schema["components"]["schemas"]

    # Remove HTTPValidationError and ValidationError
    schemas.pop("HTTPValidationError")
    schemas.pop("ValidationError")

    # Only get the keys that end in "Response"
    schemas = {k.replace("Response", "").lower() + "s": v for k, v in schemas.items() if k.endswith("Response")}

    # Format the schemas
    for schema in schemas:
        # Get the properties
        properties = schemas[schema]["properties"]

        # Create a new schema
        new_schema = {}

        # Add the properties to the new schema
        for key in properties:
            new_schema[key] = properties[key]["type"]

        # Update the schema
        schemas[schema] = new_schema

    # Return the schemas
    return schemas