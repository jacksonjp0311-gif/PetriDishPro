const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('petri', {
  runPreset: (preset, overrides) => ipcRenderer.invoke('petri:runPreset', preset, overrides || {}),
  readLatest: () => ipcRenderer.invoke('petri:readLatest'),
  openArtifactsPath: () => ipcRenderer.invoke('petri:openArtifactsPath')
});
