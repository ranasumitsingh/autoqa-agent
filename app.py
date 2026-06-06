from fastapi import FastAPI
from graphs.workflow import graph

app = FastAPI()

import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)
@app.post("/analyze")
def analyze(log_text: str):

    result = graph.invoke(
        {
            "log_text": log_text
        }
    )

    return {
        "failures": result["results"]
    }