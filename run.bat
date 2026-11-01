@echo off
title TOUCH-LAM32 Server
color 0A
echo =======================================================
echo           DEMARRAGE DU SERVEUR TOUCH-LAM32
echo =======================================================
echo.

:: Vérification de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe sur ce PC.
    echo Veuillez telecharger Python sur https://www.python.org/downloads/
    echo IMPORTANT : Cochez "Add Python to PATH" lors de l'installation.
    pause
    exit
)

:: Installation des dependances
echo Verification des dependances (peut prendre quelques secondes)...
python -m pip install -r requirements.txt --quiet

:: Lancement du serveur
echo.
python server.py

pause