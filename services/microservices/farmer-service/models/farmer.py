from pydantic import BaseModel, Field
from typing import List, Optional

class Farmer(BaseModel):
    id: str = Field(..., description="Unique identifier for the farmer")
    name: str = Field(..., description="Name of the farmer")
    email: str = Field(..., description="Email address of the farmer")
    farm_location: str = Field(..., description="Location of the farm")
    crops: List[str] = Field(..., description="List of crops grown by the farmer")
    registration_date: str = Field(..., description="Date of registration")

class FarmerCreate(BaseModel):
    name: str = Field(..., description="Name of the farmer")
    email: str = Field(..., description="Email address of the farmer")
    farm_location: str = Field(..., description="Location of the farm")
    crops: List[str] = Field(..., description="List of crops grown by the farmer")
