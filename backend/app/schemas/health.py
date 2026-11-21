from pydantic import BaseModel, Field
from datetime import datetime


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Current operational status of API")
    service: str = Field(description="Name of the running service")
    version: str = Field(description="Semantic version of API")
    environment: str = Field(description="Current running environment")
    timestamp: datetime = Field(description="UTC timestamp of the health check")
    disclaimer: str = Field(description="Academic prototype disclaimer")

