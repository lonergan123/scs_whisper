import logging
import sys
import numpy as np
from fastapi import FastAPI, Request
# open-ai-whisper package wants to communicate with the internet, and so using a local copy of core.py, as per approach from Michael Gorkow
from openai_whisper.core import transcribe

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

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/echo")
async def echo(request: Request):
   request_body = await request.json()
   request_body = request_body['data']
   return request_body

@app.get("/readstage")
async def readstage():  
    f = open('/audio_files/test_stage_file.txt', 'r')
    file_contents = f.read()
    return file_contents

@app.post("/transcripe_stage_audio")
async def transcripe_stage_audio(request: Request):
   request_body = await request.json()
   audio_file_path = request_body['audio_file_path']
   #from request body get the value of audio_file_path
   whisper_result = transcribe(audio_file_path)
   return whisper_result['text']