const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('petri', { readLatest: () => ipcRenderer.invoke('petri:readLatest'), runPreset: (payload) => ipcRenderer.invoke('petri:runPreset', payload) });
