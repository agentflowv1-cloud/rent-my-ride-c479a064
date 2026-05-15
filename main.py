from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

class Vehicle(BaseModel):
    id: int
    name: str
    features: List[str]
    availability: str

# Sample in-memory data store (replace with a database in a real application)
vehicles = [
    Vehicle(id=1, name='Vehicle 1', features=['Feature 1', 'Feature 2'], availability='Available'),
    Vehicle(id=2, name='Vehicle 2', features=['Feature 3', 'Feature 4'], availability='Not Available')
]

@app.get('/vehicles/')
async def get_vehicles():
    return vehicles

@app.get('/vehicles/{vehicle_id}')
async def get_vehicle(vehicle_id: int):
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle
    return JSONResponse(content={'error': 'Vehicle not found'}, status_code=404)

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv('PORT', 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)