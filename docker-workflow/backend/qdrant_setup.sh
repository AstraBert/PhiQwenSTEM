eval "$(conda shell.bash hook)"
cd /app/
conda activate phicare-backend
echo "Activated conda environment"
python3 createStemCollection.py
echo "Created the main data collection"
python3 toDatabase.py
echo "Ingested all the data"
python3 createCache.py
echo "Created semantic cache"
conda deactivate