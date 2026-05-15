from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Vehicle(BaseModel):
    id: int
    name: str
    features: List[str]
    availability: str

@router.get('/{vehicle_id}')
async def get_vehicle(vehicle_id: int):
    # Sample in-memory data store (replace with a database in a real application)
    vehicles = [
        {'id': 1, 'name': 'Vehicle 1', 'features': ['Feature 1', 'Feature 2'], 'availability': 'Available'},
        {'id': 2, 'name': 'Vehicle 2', 'features': ['Feature 3', 'Feature 4'], 'availability': 'Not Available'}
    ]
    for vehicle in vehicles:
        if vehicle['id'] == vehicle_id:
            return vehicle
    return {'error': 'Vehicle not found'}