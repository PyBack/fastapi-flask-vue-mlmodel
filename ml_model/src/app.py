import logging

import uvicorn
import typing

from fastapi import FastAPI
from pydantic import BaseModel

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s [%(levelname)s] {%(filename)s %(lineno)d} {%(funcName)s}: %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s [%(levelname)s] {%(filename)s %(lineno)d} {%(funcName)s}: %(message)s"

logger = logging.getLogger('uvicorn.default')

app = FastAPI()


class RequestModel(BaseModel):
    ticker: str
    data: typing.List


@app.get(path="/")
def health_check():
    msg = "FastAPI Good!!"
    logger.info(msg)
    return msg


@app.post("/eps-predict/")
async def eps_predict(request: RequestModel):

    return {}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5050, log_config=log_config)
