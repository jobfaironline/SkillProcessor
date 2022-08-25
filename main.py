import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from models import ExtractKeyWordRequest, MatchingPointRequest, CVMatchingPointRequest
from services import calculate_matching_point, extract_keyword_service, calculate_matching_point_job_position

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.

app = FastAPI()


@app.post("/extract-keyword")
def extract_keyword(request: ExtractKeyWordRequest):
    try:
        result = extract_keyword_service(request.description)
        body = set()
        for skill in result['results']['full_matches']:
            body.add(skill['doc_node_value'])
        for ngram in result['results']['ngram_scored']:
            body.add(ngram['doc_node_value'])

        return {"result": body}
    except Exception as e:
        logger.error(e)


@app.get("/")
def root():
    logger.info("Hi")
    return {"result": "ok"}


@app.post("/matching-point/application")
def calculate_matching_point_handler(request: MatchingPointRequest):
    try:
        score = calculate_matching_point(request)
        logger.info(f'Calculate application with id {request.applicationId} have score {score}')
    except Exception as e:
        logger.error(e)
        return {"result": None}

    return {"result": score * 2.5}

@app.post("/matching-point/job-position")
def calculate_matching_point_handler_job_position(request: CVMatchingPointRequest):
    try:
        score = calculate_matching_point_job_position(request)
        logger.info(f'Calculate application with id {request.jobPositionId} have score {score}')
    except Exception as e:
        logger.error(e)
        return {"result": None}

    return {"result": score * 2.5}


if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv('PORT')) or 6000
    uvicorn.run("main:app", port=port)
