from fastapi import APIRouter, HTTPException, UploadFile, File
from db.supabase_client import supabase

router = APIRouter(prefix="/upload", tags=["upload"])



@router.post("/mascota-image/{mascota_id}")
async def upload_mascota_image(mascota_id: int, file: UploadFile = File(...)):
    try:
        # Leer el archivo de manera segura
        file_data = await file.read()
        
        # Intentar subir el archivo
        file_path = f"mascotas/{mascota_id}/{file.filename}"
        response = supabase.storage.from_("images").upload(file_path, file_data)
        
        # Revisar el status code de la respuesta y el contenido para errores
        response_data = response.json()
        if response.status_code != 200 or "error" in response_data:
            error_message = response_data.get("error", {}).get("message", "Error desconocido")
            raise HTTPException(status_code=400, detail=f"Error al subir la imagen: {error_message}")

        # Generar URL pública
        image_url = supabase.storage.from_("images").get_public_url(file_path)

        # Actualizar URL en la base de datos
        supabase.table("Mascotas").update({"image_url": image_url}).eq("id", mascota_id).execute()

        return {"message": "Imagen subida correctamente", "image_url": image_url}
        
    except Exception as e:
        # Registrar el error exacto para depuración
        print(f"Error en upload_mascota_image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")