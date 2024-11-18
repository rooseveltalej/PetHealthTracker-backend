from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from core.security import create_access_token, verify_password
from models.models import LoginRequest
from db.supabase_client import supabase
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/")
async def login_user(login_data: LoginRequest):
    table = "Clientes" if login_data.role == "cliente" else "Funcionario"
    response = supabase.table(table).select("*").eq("correo", login_data.correo).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    user = response.data[0]
    if not verify_password(login_data.contraseña, user["contraseña"]):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    # Generar token JWT con el rol del usuario
    if table == "Clientes":
        token = create_access_token(
            data={
                "sub": user["correo"],
                "role": "cliente",
                "nombre": user["nombre_usuario"],
                "client_id": user["id"]
            },
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": token, "token_type": "bearer"}
    token = create_access_token(
        data={
            "sub": user["correo"],
            "role": user["puesto"],
            "nombre": user["nombre"],
            "id": user["id"]
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}
