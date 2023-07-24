@echo off

if exist venv\ (
    call venv\Scripts\activate
) else (
    py -m venv venv\
    call venv\Scripts\activate
    pip install -r requirements.txt
)

py app.py