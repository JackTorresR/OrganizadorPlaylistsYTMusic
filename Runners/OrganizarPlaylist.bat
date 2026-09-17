@echo off
cd /d "%~dp0.."
start "Organizar Playlist" cmd /k "python Scripts\OrganizarPlaylist.py"
exit