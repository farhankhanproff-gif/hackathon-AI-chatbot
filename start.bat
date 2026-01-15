@echo off

REM Check if virtual environment already exists
if not exist hackathon-AI-chatbot\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv hackathon-AI-chatbot

    call hackathon-AI-chatbot\Scripts\activate.bat

    echo Installing dependencies...
    pip install -e .
    pip install groq
) else (
    call hackathon-AI-chatbot\Scripts\activate.bat
)

REM Run chatbot
aichat

pause
