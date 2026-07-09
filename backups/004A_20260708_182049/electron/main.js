const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const repoRoot = path.resolve(__dirname, '..');
const allowedPresets = new Set(['microbial_competition','antibiotic_selection','cellular_tissue','biofilm_dormancy']);
function readJson(p){ if(!fs.existsSync(p)) return null; return JSON.parse(fs.readFileSync(p,'utf8')); }
function createWindow(){ const win = new BrowserWindow({width:1320,height:820,backgroundColor:'#02040a',webPreferences:{preload:path.join(__dirname,'preload.js'),contextIsolation:true,nodeIntegration:false,sandbox:true}}); win.loadFile(path.join(__dirname,'renderer','index.html')); if(process.argv.includes('--smoke')) setTimeout(()=>app.quit(),1400); }
ipcMain.handle('petri:readLatest', async()=>{ const p=path.join(repoRoot,'reports','bio','petri_run_latest.json'); const data=readJson(p); return {ok:Boolean(data), data, path:p}; });
ipcMain.handle('petri:runPreset', async(_event,input)=>{ const preset=String(input?.preset||'microbial_competition'); const steps=Math.max(1,Math.min(Number(input?.steps||90),400)); const grid=Math.max(12,Math.min(Number(input?.grid||56),96)); if(!allowedPresets.has(preset)) return {ok:false,error:`Preset not allowed: ${preset}`}; const args=['-m','petri_lab.cli','--root','.','--preset',preset,'--steps',String(steps),'--grid',String(grid),'--json']; return await new Promise(resolve=>{ const child=spawn('python',args,{cwd:repoRoot,shell:false,windowsHide:true,env:{...process.env,PYTHONUTF8:'1'}}); let stdout='',stderr=''; child.stdout.on('data',c=>stdout+=c.toString()); child.stderr.on('data',c=>stderr+=c.toString()); child.on('close',code=>{ if(code!==0){resolve({ok:false,code,stdout,stderr});return;} const p=path.join(repoRoot,'reports','bio','petri_run_latest.json'); resolve({ok:true,code,stdout,data:readJson(p)}); }); }); });
app.whenReady().then(createWindow); app.on('window-all-closed',()=>{ if(process.platform!=='darwin') app.quit(); }); app.on('activate',()=>{ if(BrowserWindow.getAllWindows().length===0) createWindow(); });
