from fastapi import APIRouter, HTTPException, UploadFile, File
from db.supabase_client import supabase

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/mascota-image/{mascota_id}")
async def upload_mascota_image(mascota_id: int, file: UploadFile = File(...)):
    try:
        # Read the file safely
        file_data = await file.read()

        # Proceed with the upload in storage
        file_path = f"mascotas/{mascota_id}/{file.filename}"
        response = supabase.storage.from_("images").upload(file_path, file_data)

        # Check for errors in the response
        if response.error:
            error_message = response.error.message
            raise HTTPException(status_code=400, detail=f"Error uploading image: {error_message}")

        # Generate public URL for the image
        image_url = supabase.storage.from_("images").get_public_url(file_path)

        # Update the image URL in the database
        supabase.table("Mascotas").update({"image_url": image_url}).eq("id", mascota_id).execute()
        print("Imagen actualizada")

        return {"message": "Imagen subida correctamente", "image_url": image_url}

    except Exception as e:
        # Log the exact error for debugging
        print(f"Error en upload_mascota_image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
