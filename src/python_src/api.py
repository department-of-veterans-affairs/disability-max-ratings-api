import uvicorn
from fastapi import FastAPI
from pydantic_models import (
    HealthCheckErrorResponse,
    MaxRatingsForClaimForIncreaseRequest,
    MaxRatingsForClaimForIncreaseResponse,
    Rating,
)
from starlette.responses import JSONResponse
from util.logger import logger
from util.lookup_table import MAX_RATINGS_BY_CODE, get_max_rating
from util.sanitizer import sanitize

from src.python_src.pydantic_models import HealthCheckResponse

app = FastAPI(
    title='Disability Max Ratings API',
    description='Maps a list of disabilities to their max rating.',
    contact={},
    version='v0.1',
    license={
        'name': 'CCO 1.0',
        'url': 'https://github.com/department-of-veterans-affairs/disability-max-ratings-api/blob/main/LICENSE.md',
    },
    servers=[
        {
            'url': '/',
            'description': 'Disability Max Ratings API',
        },
    ],
)


@app.get(
    '/health',
    response_model=HealthCheckResponse,
    responses={
        200: {'description': 'API is healthy', 'model': HealthCheckResponse},
        500: {'description': 'API is unhealthy', 'model': HealthCheckErrorResponse},
    },
    response_model_exclude_none=True,
)
async def get_health_status() -> HealthCheckResponse | JSONResponse:
    if not MAX_RATINGS_BY_CODE:
        return JSONResponse(
            status_code=500, content={'status': 'unhealthy', 'details': 'Max Rating by Diagnostic Code Lookup table is empty.'}
        )

    return HealthCheckResponse(status='ok')


# TODO: Update API gateway configuration when migrating to VA.gov cloud.
# The path '/disability-max-ratings' is designed to be more descriptive and domain-specific,
# replacing the legacy '/cfi/max-ratings' path that was specific to LHDI cloud.
# This will require new API gateway configuration in the VA.gov cloud environment. For more details, see: https://github.com/department-of-veterans-affairs/abd-vro/issues/3850
@app.post(
    '/disability-max-ratings',
    response_model=MaxRatingsForClaimForIncreaseResponse,
    responses={
        200: {
            'description': 'Max Ratings for Claim for Increase',
            'content': {'application/json': {'example': {'ratings': [{'diagnostic_code': 6260, 'max_rating': 10}]}}},
        },
        400: {'description': 'Invalid diagnostic code(s) received.'},
    },
)
async def get_max_ratings(
    claim_for_increase: MaxRatingsForClaimForIncreaseRequest,
) -> MaxRatingsForClaimForIncreaseResponse | JSONResponse:
    ratings = []

    diagnostic_codes = set(claim_for_increase.diagnostic_codes)

    if not has_valid_diagnostic_codes(diagnostic_codes):
        return JSONResponse(status_code=400, content={'detail': 'Invalid diagnostic code(s) received.'})

    for dc in diagnostic_codes:
        max_rating = get_max_rating(dc)
        if max_rating is not None:
            rating = Rating(diagnostic_code=int(sanitize(dc)), max_rating=max_rating)
            ratings.append(rating)

    response = MaxRatingsForClaimForIncreaseResponse(ratings=ratings)

    logger.info(f'event=getMaxRating response={response.model_dump_json()}')
    return response


# Rough boundaries of diagnostic codes as shown by document at
# (https://www.ecfr.gov/current/title-38/part-4/appendix-Appendix B to Part 4)
# TODO should be replaced with map of valid diagnostic codes and checked to see if the dc is in map.
def has_valid_diagnostic_codes(diagnostic_codes: set[int]) -> bool:
    return all(5000 <= dc <= 10000 for dc in diagnostic_codes)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8130)
