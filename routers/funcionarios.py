from fastapi import APIRouter, HTTPException, Depends
from models.models import Funcionario
from db.supabase_client import supabase
from core.security import hash_password, verify_token

router = APIRouter(prefix="/funcionarios", tags=["funcionarios"])

@router.get("/", dependencies=[Depends(verify_token)])
async def get_funcionarios():
    try:
        response = supabase.table("Funcionario").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_funcionario(funcionario: Funcionario):
    try:
        
        hashed_password = hash_password(funcionario.contraseña)
        funcionario_data = funcionario.dict()
        funcionario_data["contraseña"] = hashed_password
        response = supabase.table("Funcionario").insert(funcionario_data).execute()
        return {"message": "Funcionario creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
