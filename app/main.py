import logging
import sys
import numpy as np
from fastapi import FastAPI, Request, Query
#from whisper import tokenizer
#from openai_whisper.core import transcribe, language_detection, load_audio

# Logging
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   handler = logging.StreamHandler(sys.stdout)
   handler.setLevel(logging.DEBUG)
   handler.setFormatter(
      logging.Formatter(
      '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
   logger.addHandler(handler)
   return logger
logger = get_logger('snowpark-container-service')

#LANGUAGE_CODES=sorted(list(tokenizer.LANGUAGES.keys()))

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/transcribe")
async def transcribe():
    return {"message": "Hello Transcription!"}

@app.post("/echo")
async def echo(request: Request):
   request_body = await request.json()
   request_body = request_body['data']
   return request_body