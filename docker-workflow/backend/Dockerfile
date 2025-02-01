FROM condaforge/miniforge3:latest

WORKDIR /app/
COPY ./ /app/

RUN bash /app/conda_env.sh
RUN bash /app/qdrant_setup.sh

CMD ["bash", "/app/run.sh"]
