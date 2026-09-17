@echo off
cd /d "%~dp0.."
start "Analisar Playlist" cmd /k "python Scripts\AnalisarPlaylist.py"
exit