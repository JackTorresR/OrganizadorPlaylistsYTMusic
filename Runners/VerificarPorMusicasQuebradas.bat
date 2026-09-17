@echo off
cd /d "%~dp0.."
start "Verificar Músicas Quebradas" cmd /k "python Scripts\VerificarMusicasQuebradas.py"
exit