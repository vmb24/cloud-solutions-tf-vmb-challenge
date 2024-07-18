from pydantic import BaseModel, Field
from typing import List, Optional

class EquipmentHealth(BaseModel):
    id: str = Field(..., description="Unique identifier for the equipment health record")
    farm_id: str = Field(..., description="Unique identifier for the farm")
    equipment_type: str = Field(..., description="Type of the equipment")
    health_status: str = Field(..., description="Health status of the equipment")
    issues: Optional[List[str]] = Field(None, description="List of detected issues")
    date_checked: str = Field(..., description="Date when the health was checked")

class EquipmentHealthCreate(BaseModel):
    farm_id: str = Field(..., description="Unique identifier for the farm")
    equipment_type: str = Field(..., description="Type of the equipment")
    health_status: str = Field(..., description="Health status of the equipment")
    issues: Optional[List[str]] = Field(None, description="List of detected issues")
