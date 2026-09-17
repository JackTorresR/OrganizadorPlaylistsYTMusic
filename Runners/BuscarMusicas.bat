@echo off
cd /d "%~dp0.."
start "Buscar Musicas" cmd /c "python Scripts\BuscarMusicas.py"
exit