import httpx
import os
import asyncio
from pathlib import Path
import sys
import time
from fastapi import HTTPException

current_file_path = Path(__file__).resolve()
project_directory = current_file_path.parent.parent.parent / "AI-Module"
print(current_file_path)
print(project_directory)
sys.path.append(str(project_directory))
sys.path.append(str(project_directory / "Modules"))

from main import main as translate

async def manage_video(id:int, path:str):
    try:
        print("entre", id, path)
        translation = translate(path)
        print("pre", translation)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:3000/{id}/texto", #Cambiar a la ruta del back https://sign-ai-web.vercel.app/{id}/texto https://signai-ml.onrender.com/prueba
                json={"id": id, "translation": translation},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        print("mande")
        return
    except Exception as e:
        msg_error = "Hubo un error al traducir el video. Por favor volver a intentarlo."
        print(str(e))
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:3000/{id}/texto", #Cambiar a la ruta del back https://sign-ai-web.vercel.app/{id}/texto http://localhost:3000/{id}/texto
                json={"id": id,"translation": msg_error},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        return {"error": str(e)}

async def post_translate(body: dict) -> dict:
    url = body.url
    id = body.id
    
    if not url or not id:
        return {"error": "Faltan datos"}
    download = project_directory / "Resources" / "Downloads"
    download_path = project_directory / "Resources" / "Downloads" / f"{id},{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    try:
        already_downloaded = False
        print("pre-download")
        if not os.path.exists(download_path):
            os.makedirs(str(download), exist_ok=True)
            print("downloading")
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                with open(download_path, "wb") as f:
                    f.write(response.content)
        else:
            already_downloaded = True
        print("after download")
        asyncio.create_task(manage_video(id, download_path))
        print("task created")
        return {"message": "received", "body": body, "already_downloaded": already_downloaded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))