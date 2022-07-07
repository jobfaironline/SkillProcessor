from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np


import app as myapp

app = FastAPI()


class Request(BaseModel):
    description: str = ""

@app.post("/extract-keyword")
async def read_root(request: Request):
    result = myapp.sequential_main(request.description)
    body = set()
    for skill in result['results']['full_matches']:
        body.add(skill['doc_node_value'])
    for ngram in result['results']['ngram_scored']:
        body.add(ngram['doc_node_value'])

    return {"result": body}
