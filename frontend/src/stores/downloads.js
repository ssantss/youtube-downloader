import { writable } from 'svelte/store';

// Cargar datos del localStorage
const storedDownloads = localStorage.getItem('downloadHistory');
const initialDownloads = storedDownloads ? JSON.parse(storedDownloads) : [];

export const downloads = writable(initialDownloads);

// Suscribirse a cambios para actualizar localStorage
downloads.subscribe(value => {
  localStorage.setItem('downloadHistory', JSON.stringify(value));
});

export const addDownload = (download) => {
  downloads.update(items => {
    const newItems = [{
      id: Date.now(),
      downloadDate: new Date().toISOString(),
      ...download
    }, ...items];
    
    // Mantener solo los últimos 10 items
    return newItems.slice(0, 10);
  });
}; 