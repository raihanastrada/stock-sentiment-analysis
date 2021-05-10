echo creating virtual environment
python -m venv env
.\\env\\Scripts\\activate
echo installing requirements
pip install -r requirements.txt
echo running the program
python src/main.py