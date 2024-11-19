from fastapi import APIRouter, HTTPException, Depends
from models.models import Diagnostico, CompleteCitaData
from db.supabase_client import supabase
from core.security import verify_token

router = APIRouter(prefix="/diagnosticos", tags=["diagnosticos"])

@router.post("/", dependencies=[Depends(verify_token)])
async def create_diagnostico(diagnostico: Diagnostico):
    try:
        response = supabase.table("Diagnosticos").insert(diagnostico.dict()).execute()
        return {"message": "Diagnóstico creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/citas/{id_cita}/completar", dependencies=[Depends(verify_token)])
async def completar_cita(id_cita: int, data: CompleteCitaData):
    try:
        cita_response = supabase.table("Citas").select("*").eq("id", id_cita).execute()
        if not cita_response.data:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        cita = cita_response.data[0]
        historial_data = {
            "id_mascota": cita["id_mascota"],
            "fecha": cita["fecha_cita"],
            "tipo": data.tipo,
            "descripcion": data.motivo,
            "veterinario_id": cita["id_veterinario"],
            "resultado": data.resultado
        }
        historial_response = supabase.table("Historial").insert(historial_data).execute()
        if not historial_response.data:
            raise HTTPException(status_code=500, detail="No se pudo registrar la cita en el historial")
        delete_response = supabase.table("Citas").delete().eq("id", id_cita).execute()
        if not delete_response.data:
            raise HTTPException(status_code=500, detail="No se pudo eliminar la cita de la tabla de citas")
        return {"message": "Cita completada y movida al historial exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/historial/{id_mascota}", dependencies=[Depends(verify_token)])
async def get_historial_mascota(id_mascota: int):
    try:
        response = supabase.table("Historial").select("*").eq("id_mascota", id_mascota).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
