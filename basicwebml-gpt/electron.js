const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let backendProcess;

function waitForBackend(url, attempts = 30) {
  return new Promise((resolve, reject) => {
    let count = 0;
    const timer = setInterval(() => {
      http.get(url, () => {
        clearInterval(timer);
        resolve();
      }).on('error', () => {
        count++;
        if (count >= attempts) {
          clearInterval(timer);
          reject(new Error('Backend not responding'));
        }
      });
    }, 1000);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  win.loadFile(path.join(__dirname, 'frontend', 'build', 'index.html'));
}

app.whenReady().then(async () => {
  const backendExe = path.join(__dirname, 'backend.exe');
  backendProcess = spawn(backendExe);

  try {
    await waitForBackend('http://localhost:8000/health');
  } catch (err) {
    console.error(err);
  }

  createWindow();
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
