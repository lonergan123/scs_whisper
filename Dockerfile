FROM nvcr.io/nvidia/pytorch:23.08-py3 

# Install FFMPEG
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install fastapi gunicorn uvicorn[standard] ffmpeg-python openai-whisper

COPY . .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "1", "--timeout", "0", "main:app", "-k", "uvicorn.workers.UvicornWorker"]