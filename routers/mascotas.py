from fastapi import APIRouter, HTTPException, Depends
from models.models import Mascota
from db.supabase_client import supabase
from core.security import verify_token

router = APIRouter(prefix="/mascotas", tags=["mascotas"])

@router.get("/", dependencies=[Depends(verify_token)])
async def get_mascotas():
    try:
        response = supabase.table("Mascotas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", dependencies=[Depends(verify_token)])
async def create_mascota(mascota: Mascota):
    try:
        response = supabase.table("Mascotas").insert(mascota.dict()).execute()
        return {"message": "Mascota creada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}/editar", dependencies=[Depends(verify_token)])
async def update_mascota(id: int, mascota: Mascota):
    try:
        response = supabase.table("Mascotas").update(mascota.dict()).eq("id", id).execute()
        return {"message": "Mascota actualizada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
