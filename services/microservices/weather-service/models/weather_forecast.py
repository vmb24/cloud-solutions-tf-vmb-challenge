from pydantic import BaseModel, Field

class WeatherForecast(BaseModel):
    id: str = Field(..., description="Unique identifier for the weather forecast")
    farm_id: str = Field(..., description="Unique identifier for the farm")
    date: str = Field(..., description="Date of the forecast")
    temperature: float = Field(..., description="Forecasted temperature")
    humidity: float = Field(..., description="Forecasted humidity level")
    precipitation: float = Field(..., description="Forecasted precipitation level")
    wind_speed: float = Field(..., description="Forecasted wind speed")

class WeatherForecastCreate(BaseModel):
    farm_id: str = Field(..., description="Unique identifier for the farm")
    date: str = Field(..., description="Date of the forecast")
    temperature: float = Field(..., description="Forecasted temperature")
    humidity: float = Field(..., description="Forecasted humidity level")
    precipitation: float = Field(..., description="Forecasted precipitation level")
    wind_speed: float = Field(..., description="Forecasted wind speed")
