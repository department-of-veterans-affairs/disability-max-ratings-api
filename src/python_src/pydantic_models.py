from pydantic import BaseModel, Field, conint
from typing_extensions import Annotated


class MaxRatingsForClaimForIncreaseRequest(BaseModel):
    diagnostic_codes: Annotated[list[conint(strict=True, ge=5000, le=10000)], Field(max_length=1000)]


class Rating(BaseModel):
    diagnostic_code: int
    max_rating: int


class MaxRatingsForClaimForIncreaseResponse(BaseModel):
    ratings: list[Rating] = []


class HealthCheckResponse(BaseModel):
    status: str = Field(examples=['ok'])


class HealthCheckErrorResponse(BaseModel):
    status: str = Field(examples=['unhealthy'])
    details: str = Field(examples=['Max Rating by Diagnostic Code Lookup table is empty.'])
