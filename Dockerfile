FROM nvcr.io/nvidia/pytorch:23.08-py3 

RUN pip install fastapi gunicorn uvicorn[standard]

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "1", "--timeout", "0", "main:app", "-k", "uvicorn.workers.UvicornWorker"]