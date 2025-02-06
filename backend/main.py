from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
from typing import Optional
import asyncio
from download import download_video
import os
from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv

app = FastAPI()

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cuidado: solo para desarrollo local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class VideoURL(BaseModel):
    url: str

class DownloadProgress:
    def __init__(self):
        self.progress = 0
        self.status = "waiting"
        self.filename = ""

    def update(self, d):
        if d['status'] == 'downloading':
            self.progress = float(d['downloaded_bytes']*100/d['total_bytes'])
            self.status = "downloading"
            self.filename = d['filename']
        elif d['status'] == 'finished':
            self.status = "finished"

@app.get("/")
async def read_root():
    return {"message": "YouTube Downloader API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            # Manejar mensajes del cliente
            await websocket.send_json({"progress": download_progress.progress})
        except Exception:
            break

@app.post("/download/")
async def start_download(video: VideoURL, background_tasks: BackgroundTasks):
    file_path = None
    try:
        file_path, original_filename = await asyncio.to_thread(download_video, video.url)
        
        # Debug: ver qué nombre estamos enviando
        print(f"Original filename: {original_filename}")
        encoded_filename = quote(original_filename)
        print(f"Encoded filename: {encoded_filename}")
        
        def iterfile():
            with open(file_path, mode="rb") as file_like:
                yield from file_like

        def cleanup(filepath: str):
            Path(filepath).unlink(missing_ok=True)

        # Asegurar que el header está correctamente formateado
        headers = {
            "Content-Disposition": f'attachment; filename*=UTF-8\'\'{encoded_filename}',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
        
        response = StreamingResponse(
            iterfile(),
            media_type="video/mp4",
            headers=headers
        )
        
        background_tasks.add_task(cleanup, file_path)
        return response
    except Exception as e:
        # Si hay error, intentar limpiar el archivo si existe
        if file_path:
            Path(file_path).unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(e))

load_dotenv('../.env')

PORT = int(os.getenv('BACKEND_PORT', 8765))
HOST = os.getenv('HOST_IP', '0.0.0.0')

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)