from fastapi import APIRouter, HTTPException, Depends
from db.supabase_client import supabase
from core.security import verify_token

router = APIRouter(prefix="/vacunas", tags=["vacunas"])

@router.get("/{id_vacuna}", dependencies=[Depends(verify_token)])
async def get_vacuna(id_vacuna: int):
    try:
        response = supabase.table("Vacunas").select("*").eq("id", id_vacuna).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mascotas/{id_mascota}", dependencies=[Depends(verify_token)])
async def get_vacunas_mascota(id_mascota: int):
    try:
        response = supabase.from_("VacunasMascotas").select("*").filter("mascota", "eq", id_mascota).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/asociar", dependencies=[Depends(verify_token)])
async def associate_pet_vaccine(mascota_id: int, vacuna_id: int):
    try:
        data = {
            "mascota": mascota_id,
            "vacuna": vacuna_id
        }
        response = supabase.table("VacunasMascotas").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="No se pudo asociar la vacuna a la mascota.")
        return {"message": "Mascota y vacuna asociadas correctamente", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
