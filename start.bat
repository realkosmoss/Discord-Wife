@echo off
set VENV_DIR=venv

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate

pip install -r requirements.txt

echo Running main.py
python main.py


cmd /k
