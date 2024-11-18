from fastapi import APIRouter, HTTPException
from models.models import Cliente
from db.supabase_client import supabase
from core.security import hash_password

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/")
async def get_clientes():
    try:
        response = supabase.table("Clientes").select("id, nombre_usuario, correo").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_cliente(cliente: Cliente):
    try:
        hashed_password = hash_password(cliente.contraseña)
        cliente_data = cliente.dict()
        cliente_data["contraseña"] = hashed_password
        response = supabase.table("Clientes").insert(cliente_data).execute()
        return {"message": "Cliente creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
