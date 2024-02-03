import numpy as np
from fastapi import FastAPI, Request
import whisper 

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

@app.get("/readstage")
async def readstage():  
    f = open('/audio_files/test_stage_file.txt', 'r')
    file_contents = f.read()
    return file_contents

@app.get("/transcripe_stage_audio")
async def transcripe_stage_audio():  
    model = whisper.load_model("tiny.en", download_root="/whisper_models")
    result = model.transcribe("/audio_files/SampleMedDictation.mp3")
    return result["text"]