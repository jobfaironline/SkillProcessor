python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
pip install "uvicorn[standard]"
uvicorn main:app --reload --port 6000
