from fastapi import FastAPI, UploadFile

from app.services.gemini import analyze_photo_image

app = FastAPI()

@app.post("/analyze")
async def create_upload_file(file: UploadFile):
    file_image_bytes = await file.read()
    return await analyze_photo_image(file_image_bytes)
