# set up the venv for the project
# Usage: source activate.sh

# see if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# activate the venv
source venv/bin/activate
pip install -r requirements.txt
