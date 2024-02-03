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

def load_audio(file: str, encode=True, sr: int = 16000):
    """
    Open an audio file object and read as mono waveform, resampling as necessary.
    Parameters
    ----------
    encode: Boolean
        If true, encode audio stream to WAV before sending to whisper
    sr: int
        The sample rate to resample the audio if necessary
    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
  
    if encode:
        try:
            # ffmpeg to read audio data from requests
            cmd = [
                "ffmpeg",
                "-nostdin",
                "-threads", "0",
                "-i", file,
                "-f", "s16le",
                "-ac", "1",
                "-acodec", "pcm_s16le",
                "-ar", str(16000),
                "-"
            ]
            out = run(cmd, capture_output=True, check=True).stdout
        except Exception as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

def transcribe():
    with model_lock:
        result = model.transcribe("/audio_files/SampleMedDictation.mp3")
    return result
