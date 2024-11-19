from fastapi import APIRouter, HTTPException, Depends
from models.models import Cita, CompleteCitaData
from db.supabase_client import supabase
from core.security import verify_token

router = APIRouter(prefix="/citas", tags=["citas"])

@router.get("/", dependencies=[Depends(verify_token)])
async def get_citas():
    try:
        response = supabase.table("Citas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", dependencies=[Depends(verify_token)])
async def get_citas_mascota(id: int):
    try:
        response = supabase.table("Citas").select("*").eq("id_mascota", id).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Esta ruta no obtiene la cita por medio de la fecha de la cita, sino por el id, el nombre es para evitar conflictos con el frontend.
#Por ende, esta función obtiene la cita por medio del id de la cita.
@router.get("/{id}/fecha", dependencies=[Depends(verify_token)])
async def get_citas_fecha(id: int):
    try:
        response = supabase.table("Citas").select("*").eq("id", id).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/veterinario/{id}", dependencies=[Depends(verify_token)])
async def get_citas_veterinario(id: int):
    try:
        response = supabase.table("Historial").select("*").eq("veterinario_id", id).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", dependencies=[Depends(verify_token)])
async def create_cita(cita: Cita):
    try:
        response = supabase.table("Citas").insert(cita.dict()).execute()
        return {"message": "Cita creada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{id_cita}/completar", dependencies=[Depends(verify_token)])
async def completar_cita(id_cita: int, data: CompleteCitaData):
    try:
        # Obtenenemos la cita
        cita_response = supabase.table("Citas").select("*").eq("id", id_cita).execute()
        
        if not cita_response.data:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        cita = cita_response.data[0]

        # Preparar datos para insertar en Historial usando los datos proporcionados
        historial_data = {
            "id_mascota": cita["id_mascota"],
            "fecha": cita["fecha_cita"],
            "tipo": data.tipo,
            "descripcion": data.motivo,
            "veterinario_id": cita["id_veterinario"],
            "resultado": data.resultado
        }

        # Insertar la cita en el historial
        historial_response = supabase.table("Historial").insert(historial_data).execute()
        
        if not historial_response.data:
            raise HTTPException(status_code=500, detail="No se pudo registrar la cita en el historial")

        # Eliminar la cita de la tabla de citas
        delete_response = supabase.table("Citas").delete().eq("id", id_cita).execute()
        
        if not delete_response.data:
            raise HTTPException(status_code=500, detail="No se pudo eliminar la cita de la tabla de citas")

        return {"message": "Cita completada y movida al historial exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {str(e)}")

@router.delete("/{id_cita}/cancelar", dependencies=[Depends(verify_token)])
async def cancelar_cita(id_cita: int):
    try:
        response = supabase.table("Citas").delete().eq("id", id_cita).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Cita no encontrada o no pudo ser cancelada")
        return {"message": "Cita cancelada exitosamente", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error al cancelar la cita.")
