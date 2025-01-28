<h1 align="center">PhiCare</h1>
<h2 align="center">An assistant for your medical cases</h2>
<div align="center">
    <img src="./PhiCare.png" alt="PhiCare Logo">
</div>

**PhiCare** is an assistant aimed at resolving medical cases. It is based on **Phi-3.5** by Microsoft, provided by [HuggingFace](https://huggingface.co) Inference API, and has a vast knowledge base (almost 25000 data points) managed via [Qdrant](https://qdrant.tech).

## Workflow

![PhiCare Workflow](./PhiCare_workflow.png)

## Installation and usage

### 1. Docker

> _Required: [Docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/)_

- Clone this repository

```bash
git clone https://github.com/AstraBert/PhiCare.git
cd PhiCare/docker
```

- Add the `hf_token` secret in the [`.env.example`](./docker/.env.example) file and modify the name of the file to `.env`. You can get your HuggingFace token by [registering](https://huggingface.co/join) to HuggingFace and creating a [fine-grained token](https://huggingface.co/settings/tokens) that has access to the Inference API.

```bash
# modify your access token, e.g. hf_token="hf_abcdefg1234567"
mv .env.example .env
```

- Launch the docker application:

```bash
# The -d option is not mandatory
docker compose up -d
```

## Local

> _Required: [Docker](https://docs.docker.com/desktop/), [docker compose](https://docs.docker.com/compose/) and [conda](https://anaconda.org/anaconda/conda)_

- Clone this repository

```bash
git clone https://github.com/AstraBert/PhiCare.git
cd PhiCare/local
```

- If you are on Linux, you can run:

```bash
bash local_setup.sh
```

- If you are on macOS/Windows, running all the commands separately might be optimal:

```bash
# Launch Qdrant
docker compose up -d

# Create conda environment for the backend
conda env create -f ./backend/environment.yml
conda activate phicare-backend

# Ingest data
python3 data/toDatabase.py

# Create a semantic cache
python3 data/createCache.py

conda deactivate

# Install necessary dependencies for the UI
cd chatbot-ui/
npm install

# Back to the local folder
cd ..
```

- Once you are done with the set-up, launch the UI:

```bash
cd chatbot-ui/
npm run dev
```

- And, on a separate terminal window, launch the backend:

```bash
conda activate phicare-backend
cd backend/
python3 backend.py
```

Head over to http://localhost:8501 and you should see PhiCare up and running in less than one minute!

## Contributions

Contributions are more than welcome! See [contribution guidelines](./CONTRIBUTING.md) for more information :)

## Funding

If you found this project useful, please consider to [fund it](https://github.com/sponsors/AstraBert) and make it grow: let's support open-source together!😊

## License and usage guidelines




