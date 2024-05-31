import requests
from typing import Union, List, Dict

def create_record(table_name: str, data: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
    """
    Create a record in the database. 
    
    The data should be in the format:
    - For cars:
    {
        "make": str,
        "model": str,
        "year": int
    }
    - For drivers:
    {
        "name": str,
        "license_number": str,
        "car_id": int
    }
    """
    BASE_URL = "http://localhost:8000"  # Update with your FastAPI app's URL
    url = f"{BASE_URL}/{table_name}/"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error creating {table_name}: {response.text}")

def read_records(table_name: str) -> List[Dict[str, Union[str, int]]]:
    """
    Read all records from the database.
    """
    BASE_URL = "http://localhost:8000"  # Update with your FastAPI app's URL
    url = f"{BASE_URL}/{table_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error reading {table_name}: {response.text}")

def update_record(table_name: str, record_id: int, data: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
    """
    Update a record in the database.

    The data should contain:
     - For cars:
    {
        "make": str,
        "model": str,
        "year": int
    }
    - For drivers:
    {
        "name": str,
        "license_number": str,
        "car_id": int
    }
    """
    BASE_URL = "http://localhost:8000"  # Update with your FastAPI app's URL
    url = f"{BASE_URL}/{table_name}/{record_id}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error updating {table_name} with ID {record_id}: {response.text}")

def delete_record(table_name: str, record_id: int) -> Dict[str, str]:
    """
    Delete a record from the database.
    """
    BASE_URL = "http://localhost:8000"  # Update with your FastAPI app's URL
    url = f"{BASE_URL}/{table_name}/{record_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error deleting {table_name} with ID {record_id}: {response.text}")