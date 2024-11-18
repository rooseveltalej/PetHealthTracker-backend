from fastapi import APIRouter, HTTPException, UploadFile, File
from db.supabase_client import supabase

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/mascota-image/{mascota_id}")
async def upload_mascota_image(mascota_id: int, file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        file_path = f"mascotas/{mascota_id}/{file.filename}"
        response = supabase.storage.from_("images").upload(file_path, file_data)
        response_data = response.json()
        if response.status_code != 200 or "error" in response_data:
            error_message = response_data.get("error", {}).get("message", "Error desconocido")
            raise HTTPException(status_code=400, detail=f"Error al subir la imagen: {error_message}")
        image_url = supabase.storage.from_("images").get_public_url(file_path)
        supabase.table("Mascotas").update({"image_url": image_url}).eq("id", mascota_id).execute()
        return {"message": "Imagen subida correctamente", "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
