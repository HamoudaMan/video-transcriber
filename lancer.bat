@echo off
title Transcription YouTube
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 goto need_installer

python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 goto need_installer

python -c "import whisper" >nul 2>&1
if errorlevel 1 goto need_installer

echo Mise a jour de yt-dlp (pour rester compatible avec TikTok/YouTube)...
python -m pip install -U yt-dlp >nul 2>&1

python transcrire.py
goto :eof

:need_installer
echo.
echo [ERREUR] L'installation n'est pas complete.
echo Double-clique d'abord sur installer.bat, attends qu'il affiche
echo "INSTALLATION TERMINEE", puis reessaie de lancer ce fichier.
echo.
pause
