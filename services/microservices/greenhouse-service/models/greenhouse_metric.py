from pydantic import BaseModel, Field

class GreenhouseMetric(BaseModel):
    id: str = Field(..., description="Unique identifier for the greenhouse metric")
    farm_id: str = Field(..., description="Unique identifier for the farm")
    temperature: float = Field(..., description="Temperature inside the greenhouse")
    humidity: float = Field(..., description="Humidity level inside the greenhouse")
    co2_level: float = Field(..., description="CO2 level inside the greenhouse")
    light_intensity: float = Field(..., description="Light intensity inside the greenhouse")
    date_collected: str = Field(..., description="Date when the metric was collected")

class GreenhouseMetricCreate(BaseModel):
    farm_id: str = Field(..., description="Unique identifier for the farm")
    temperature: float = Field(..., description="Temperature inside the greenhouse")
    humidity: float = Field(..., description="Humidity level inside the greenhouse")
    co2_level: float = Field(..., description="CO2 level inside the greenhouse")
    light_intensity: float = Field(..., description="Light intensity inside the greenhouse")
