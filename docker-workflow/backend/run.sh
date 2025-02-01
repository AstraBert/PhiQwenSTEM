eval "$(conda shell.bash hook)"
cd /app/
conda activate phicare-backend
echo "Activated conda environment"
python3 backend.py