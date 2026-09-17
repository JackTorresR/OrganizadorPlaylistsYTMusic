@echo off
cd /d "%~dp0.."
start "Remover Duplicadas" cmd /k "python Scripts\RemoverDuplicadas.py"
exit