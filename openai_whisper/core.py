import logging
import sys, os
import os
from typing import Union
from threading import Lock
import torch
import whisper
#import requests
import numpy as np
from subprocess import run

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

model_name= os.getenv("ASR_MODEL", "base")
if torch.cuda.is_available():
    logger.debug(f"Running on GPU")
    model = whisper.load_model(model_name, download_root='/whisper_models').cuda()
else:
    logger.debug(f"Running on CPU")
    model = whisper.load_model(model_name, download_root='/whisper_models')
model_lock = Lock()


def transcribe(audio_file_path: str):
    with model_lock:
        result = model.transcribe(audio_file_path)  #"/audio_files/SampleMedDictation.mp3"
    return result
