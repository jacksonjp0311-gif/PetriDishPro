const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const repoRoot = path.resolve(__dirname, '..');

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1100,
    minHeight: 760,
    backgroundColor: '#03060c',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  if (process.argv.includes('--devtools')) win.webContents.openDevTools();
}

function readJsonSafe(relativePath) {
  const target = path.join(repoRoot, relativePath);
  if (!target.startsWith(repoRoot)) throw new Error('Path escape blocked');
  if (!fs.existsSync(target)) return null;
  return JSON.parse(fs.readFileSync(target, 'utf8'));
}

function readTextSafe(relativePath) {
  const target = path.join(repoRoot, relativePath);
  if (!target.startsWith(repoRoot)) throw new Error('Path escape blocked');
  if (!fs.existsSync(target)) return '';
  return fs.readFileSync(target, 'utf8');
}

function runPython(args) {
  return new Promise((resolve) => {
    const child = spawn('python', args, {
      cwd: repoRoot,
      shell: false,
      windowsHide: true,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    let stdout = '';
    let stderr = '';
    const timer = setTimeout(() => {
      try { child.kill(); } catch (_) {}
      resolve({ ok: false, code: -1, stdout, stderr: stderr + '\nTimeout' });
    }, 120000);
    child.stdout.on('data', d => { stdout += d.toString(); });
    child.stderr.on('data', d => { stderr += d.toString(); });
    child.on('close', code => {
      clearTimeout(timer);
      resolve({ ok: code === 0, code, stdout, stderr });
    });
  });
}

ipcMain.handle('petri:runPreset', async (_event, preset, overrides) => {
  const allowed = new Set(['microbial_competition', 'cellular_tissue', 'antibiotic_selection']);
  const selected = allowed.has(preset) ? preset : 'microbial_competition';
  const args = ['-m', 'petri_lab.cli', '--root', '.', '--preset', selected, '--json'];
  if (overrides && Number.isFinite(overrides.grid)) args.push('--grid', String(overrides.grid));
  if (overrides && Number.isFinite(overrides.steps)) args.push('--steps', String(overrides.steps));
  if (overrides && Number.isFinite(overrides.seed)) args.push('--seed', String(overrides.seed));
  const result = await runPython(args);
  let payload = null;
  try { payload = JSON.parse(result.stdout); } catch (_) {}
  return { ...result, payload };
});

ipcMain.handle('petri:readLatest', async () => {
  return {
    run: readJsonSafe('reports/latest_run.json'),
    density: readJsonSafe('reports/latest_density.json'),
    validation: readJsonSafe('reports/latest_validation.json'),
    summary: readTextSafe('reports/latest_summary.md')
  };
});

ipcMain.handle('petri:openArtifactsPath', async () => {
  return path.join(repoRoot, 'artifacts', 'runs');
});

app.whenReady().then(() => {
  if (process.argv.includes('--smoke')) {
    app.exit(0);
    return;
  }
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
