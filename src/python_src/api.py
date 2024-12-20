import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic_models import (
    MaxRatingsForClaimForIncreaseRequest,
    MaxRatingsForClaimForIncreaseResponse,
    Rating,
)
from util.logger import logger
from util.lookup_table import MAX_RATINGS_BY_CODE, get_max_rating
from util.sanitizer import sanitize

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


@app.get('/health')
async def get_health_status() -> dict[str, str]:
    if not MAX_RATINGS_BY_CODE:
        raise HTTPException(status_code=500, detail='Max Rating by Diagnostic Code Lookup table is empty.')

    return {'status': 'ok'}


# TODO: Update API gateway configuration when migrating to VA.gov cloud.
# The path '/disability-max-ratings' is designed to be more descriptive and domain-specific,
# replacing the legacy '/cfi/max-ratings' path that was specific to LHDI cloud.
# This will require new API gateway configuration in the VA.gov cloud environment. For more details, see: https://github.com/department-of-veterans-affairs/abd-vro/issues/3850
@app.post('/disability-max-ratings')
async def get_max_ratings(
    claim_for_increase: MaxRatingsForClaimForIncreaseRequest,
) -> MaxRatingsForClaimForIncreaseResponse:
    ratings = []
    for dc in set(claim_for_increase.diagnostic_codes):
        validate_diagnostic_code(dc)
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
def validate_diagnostic_code(dc: int) -> None:
    if dc < 5000 or dc > 10000:
        raise HTTPException(status_code=400, detail=f'The diagnostic code received is invalid: dc={dc}')


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8130)
