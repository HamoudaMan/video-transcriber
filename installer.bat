@echo off
title Installation - Transcription YouTube
cd /d "%~dp0"

echo ============================================================
echo   INSTALLATION - Transcription YouTube / TikTok
echo   Ne ferme pas cette fenetre pendant l'installation.
echo ============================================================
echo.

REM ============================================================
REM 1. PYTHON
REM ============================================================
where python >nul 2>&1
if errorlevel 1 goto install_python
echo [1/3] Python est deja installe. OK.
goto check_ffmpeg

:install_python
echo [1/3] Python n'est pas installe. Telechargement en cours...
where curl >nul 2>&1
if errorlevel 1 goto no_curl

set PY_INSTALLER=%TEMP%\python-installer.exe
curl -L -o "%PY_INSTALLER%" "https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe"

if not exist "%PY_INSTALLER%" goto download_failed

echo Installation de Python en cours, patiente une minute...
"%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
del "%PY_INSTALLER%" >nul 2>&1

echo.
echo ============================================================
echo   Python vient d'etre installe !
echo   FERME cette fenetre, puis redouble-clique sur installer.bat
echo   pour continuer l'installation (c'est normal, il faut le
echo   faire une deuxieme fois).
echo ============================================================
pause
exit /b 0

:no_curl
echo [ERREUR] L'outil "curl" n'est pas disponible sur cet ordinateur.
echo Cet ordinateur est peut-etre trop ancien pour cette methode automatique.
echo Demande de l'aide pour installer Python manuellement depuis :
echo https://www.python.org/downloads/
echo En cochant bien la case "Add python.exe to PATH" pendant l'installation.
pause
exit /b 1

:download_failed
echo [ERREUR] Le telechargement de Python a echoue.
echo Verifie ta connexion internet, puis relance ce fichier (installer.bat).
pause
exit /b 1

REM ============================================================
REM 2. FFMPEG
REM ============================================================
:check_ffmpeg
where ffmpeg >nul 2>&1
if errorlevel 1 goto install_ffmpeg
echo [2/3] FFmpeg est deja installe. OK.
goto install_libs

:install_ffmpeg
echo [2/3] FFmpeg n'est pas installe. Installation en cours...
where winget >nul 2>&1
if errorlevel 1 goto no_winget

winget install -e --id Gyan.FFmpeg --silent --accept-package-agreements --accept-source-agreements

echo.
echo ============================================================
echo   FFmpeg vient d'etre installe !
echo   FERME cette fenetre, puis redouble-clique sur installer.bat
echo   pour continuer l'installation (c'est normal, il faut le
echo   faire une deuxieme fois).
echo ============================================================
pause
exit /b 0

:no_winget
echo [ERREUR] "winget" n'est pas disponible sur cet ordinateur.
echo Demande de l'aide pour installer FFmpeg manuellement.
pause
exit /b 1

REM ============================================================
REM 3. LIBRAIRIES PYTHON
REM ============================================================
:install_libs
echo [3/3] Installation des librairies Python (yt-dlp, Whisper)...
echo Cela peut prendre plusieurs minutes la premiere fois, merci de patienter.
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt

echo.
echo ============================================================
echo   INSTALLATION TERMINEE !
echo   Tu peux maintenant utiliser lancer.bat pour transcrire
echo   tes videos. Cette fenetre peut etre fermee.
echo ============================================================
pause
