from fastapi import FastAPI, UploadFile, HTTPException

from app.config import MAX_FILE_SIZE, SUPPORTED_CONTENT_TYPES
from app.services.gemini import analyze_photo_image, GeminiQuotaError, GeminiConfigError, GeminiUnavailableError, \
    GeminiTimeoutError
from app.utils import is_valid_image

app = FastAPI()

@app.post("/analyze")
async def create_upload_file(file: UploadFile):
    if (file.content_type or "").lower() not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="File type not supported")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    if file.size == 0:
        raise HTTPException(status_code=400, detail="No image")

    file_image_bytes = await file.read()

    if not is_valid_image(file_image_bytes):
        raise HTTPException(status_code=422, detail="Invalid image")

    try:
        return await analyze_photo_image(file_image_bytes, file.content_type)
    except GeminiQuotaError as e:
        raise HTTPException(
            status_code=503,
            detail="Сервис перегружен, попробуйте позже",
            headers={"Retry-After": "60"}
        ) from e
    except GeminiConfigError as e:
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервиса",
        ) from e
    except GeminiUnavailableError as e:
        raise HTTPException(
            status_code=502,
            detail="Сервис недоступен, попробуйте позже",
        ) from e
    except GeminiTimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail="Превышено время ожидания",
        ) from e