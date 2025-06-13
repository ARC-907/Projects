@echo off
REM Build React frontend and backend executable
cd frontend
npm install
npm run build:react
cd ..

pyinstaller --noconfirm --onefile backend_launcher.py --name backend

REM Copy backend exe into frontend for packaging
copy dist\backend.exe frontend\backend.exe >nul

cd frontend
npm run package
cd ..

echo Build complete. Check the dist folder for the installer.
