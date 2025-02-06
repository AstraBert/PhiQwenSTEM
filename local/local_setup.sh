echo "Setting up local phiSTEM"

docker compose up -d
echo "Launched Qdrant"

eval "$(conda shell.bash hook)"
conda env create -f ./backend/environment.yml
conda activate backend
echo "Created and activated conda environment"

python3 data/createStemCollection.py
echo "Created the main data collection"
python3 data/toDatabase.py
echo "Ingested all the data"
python3 data/createCache.py
echo "Created semantic cache"

conda deactivate

cd chatbot-ui/
npm install
echo "Installed all the necessary dependencies for the UI"