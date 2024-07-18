from pydantic import BaseModel, Field
from typing import Optional

class SoilMetric(BaseModel):
    id: str = Field(..., description="Unique identifier for the soil metric")
    farm_id: str = Field(..., description="Unique identifier for the farm")
    ph_level: float = Field(..., description="pH level of the soil")
    moisture_level: float = Field(..., description="Moisture level of the soil")
    temperature: float = Field(..., description="Temperature of the soil")
    date_collected: str = Field(..., description="Date when the metric was collected")

class SoilMetricCreate(BaseModel):
    farm_id: str = Field(..., description="Unique identifier for the farm")
    ph_level: float = Field(..., description="pH level of the soil")
    moisture_level: float = Field(..., description="Moisture level of the soil")
    temperature: float = Field(..., description="Temperature of the soil")
