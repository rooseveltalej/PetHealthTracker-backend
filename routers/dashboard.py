from fastapi import APIRouter, HTTPException, Depends
from db.supabase_client import supabase
from core.security import verify_token

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard_data():
    try:
        # Total de citas programadas, realizadas y pendientes
        citas = supabase.table("Citas").select("*").execute().data
        revisadas = supabase.table("Historial").select("*").execute().data
        total_citas = len(citas)
        total_revisadas = len(revisadas)
        citas_pendientes = total_revisadas - total_citas

        # Total de clientes y funcionarios
        total_clientes = len(supabase.table("Clientes").select("*").execute().data)
        total_funcionarios = len(supabase.table("Funcionario").select("*").execute().data)
        usuarios_activos = total_clientes + total_funcionarios

        # Total de mascotas
        total_mascotas = len(supabase.table("Mascotas").select("*").execute().data)

        # Promedio de citas por veterinario
        citas_por_veterinario = {}
        for cita in citas:
            vet_id = cita.get("id_veterinario")
            if vet_id:
                citas_por_veterinario[vet_id] = citas_por_veterinario.get(vet_id, 0) + 1
        promedio_citas_veterinario = sum(citas_por_veterinario.values()) / len(citas_por_veterinario) if citas_por_veterinario else 0

        return {
            "appointment_stats": {
                "scheduled": total_citas,
                "completed": total_revisadas,
                "pending": citas_pendientes,
            },
            "active_users": {
                "clients": total_clientes,
                "staff": total_funcionarios,
                "total": usuarios_activos,
            },
            "total_pets": total_mascotas,
            "avg_appointments_per_vet": promedio_citas_veterinario,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos del dashboard: {e}")