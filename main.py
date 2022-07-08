import logging
import os
import random
import string
import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from models import ExtractKeyWordRequest, MatchingPointRequest
from services import extract_keyword, calculate_matching_point

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.

app = FastAPI()


@app.middleware("http")
async def log_requests(request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.post("/extract-keyword")
async def extract_keyword(request: ExtractKeyWordRequest):
    result = extract_keyword(request.description)
    body = set()
    for skill in result['results']['full_matches']:
        body.add(skill['doc_node_value'])
    for ngram in result['results']['ngram_scored']:
        body.add(ngram['doc_node_value'])

    return {"result": body}


@app.get("/")
async def root():
    logger.info("Hi")
    return {"result": "ok"}


@app.post("/matching-point")
async def calculate_matching_point_handler(request: MatchingPointRequest):
    score = calculate_matching_point(request)
    logger.info(f'Calculate application with id {request.applicationId} have score {score}')
    return {"result": score}


if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv('PORT')) or 6000
    uvicorn.run("main:app", port=port)
