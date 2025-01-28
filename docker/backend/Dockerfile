FROM condaforge/miniforge3:latest

WORKDIR /app/
COPY ./ /app/

RUN bash /app/conda_env.sh
RUN conda activate phicare-backend
RUN python3 createCache.py
RUN python3 toDatabase.py

CMD ["python3", "/app/backend.py"]
