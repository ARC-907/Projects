BasicWebML-GPT Desktop Packaging
================================

This guide explains how to package the FastAPI backend and React frontend into a
single Windows executable using Electron and PyInstaller.

Development
-----------
1. Install Python 3.11 and Node.js (18+).
2. Install backend dependencies:
   ````
   cd backend
   pip install -r requirements.txt
   ````
3. Install frontend dependencies:
   ````
   cd ../frontend
   npm install
   ````
4. Run the backend for development:
   ````
   uvicorn app:app --reload
   ````
5. Launch the React app in a browser or run `npm start`.

Packaging
---------
1. Build the React frontend and backend executable by running `build.bat` from
the project root (Windows only).
2. `build.bat` performs the following:
   - `npm run build:react` to create the frontend bundle.
   - `pyinstaller --onefile backend_launcher.py` to create `backend.exe`.
   - Copies the build files and runs `electron-builder --win --x64` to create
     `BasicWebML-GPT.exe` in the `dist/` folder.

Usage
-----
Run the generated `BasicWebML-GPT.exe`. It automatically starts the FastAPI
server in the background and opens the Electron window that loads the React
interface. Closing the window shuts down the backend process.
