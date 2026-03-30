@echo off
cd /d "C:\Users\User\OneDrive\Documentos\Seminario\seminario"
del /f /q auth_service\auth.db 2>nul
del /f /q user_service\user.db 2>nul
del /f /q instance\auth.db 2>nul
del /f /q instance\user.db 2>nul
echo Done
python auth_service/app.py
