import bcrypt
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client
from pydantic import BaseModel

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de Pydantic para validación de datos
class Mascota(BaseModel):
    nombre_mascota: str
    especie: str
    raza: str
    fecha_nacimiento: str
    id_dueño: int

class Cliente(BaseModel):
    nombre_usuario: str
    correo: str
    contraseña: str

class Cita(BaseModel):
    id_mascota: int
    fecha_cita: str
    id_veterinario: int
    hora_cita: str

class Diagnostico(BaseModel):
    id_evaluacion: int
    diagnostico: str
    tratamiento: str

class Funcionario(BaseModel):
    nombre: str
    puesto: str
    correo: str
    contraseña: str

# Función para cifrar la contraseña
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Ruta GET para verificar la conexión a la base de datos
@app.get("/check-table/")
async def check_db(tabla: str):
    try:
        response = supabase.table(tabla).select("*").execute()
        return {"message": "Connected to the database", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints CRUD completos

# Crear una mascota
@app.post("/mascotas/")
async def create_mascota(mascota: Mascota):
    try:
        response = supabase.table("Mascotas").insert(mascota.dict()).execute()
        return {"message": "Mascota creada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener todas las mascotas
@app.get("/mascotas/")
async def get_mascotas():
    try:
        response = supabase.table("Mascotas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar información de una mascota
@app.put("/mascotas/{id}")
async def update_mascota(id: int, mascota: Mascota):
    try:
        response = supabase.table("Mascotas").update(mascota.dict()).eq('id', id).execute()
        return {"message": "Mascota actualizada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar una mascota
@app.delete("/mascotas/{id}")
async def delete_mascota(id: int):
    try:
        response = supabase.table("Mascotas").delete().eq('id', id).execute()
        return {"message": "Mascota eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agregar cliente
@app.post("/clientes/")
async def create_cliente(cliente: Cliente):
    try:
        hashed_password = hash_password(cliente.contraseña)
        cliente_data = cliente.dict()
        cliente_data["contraseña"] = hashed_password
        response = supabase.table("Clientes").insert(cliente_data).execute()
        return {"message": "Cliente creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Crear una cita
@app.post("/citas/")
async def create_cita(cita: Cita):
    try:
        response = supabase.table("Citas").insert(cita.dict()).execute()
        return {"message": "Cita creada", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener todas las citas
@app.get("/citas/")
async def get_citas():
    try:
        response = supabase.table("Citas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agregar diagnóstico
@app.post("/diagnosticos/")
async def create_diagnostico(diagnostico: Diagnostico):
    try:
        response = supabase.table("Diagnosticos").insert(diagnostico.dict()).execute()
        return {"message": "Diagnóstico creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Crear funcionario
@app.post("/funcionarios/")
async def create_funcionario(funcionario: Funcionario):
    try:
        hashed_password = hash_password(funcionario.contraseña)
        funcionario_data = funcionario.dict()
        funcionario_data["contraseña"] = hashed_password
        response = supabase.table("Funcionario").insert(funcionario_data).execute()
        return {"message": "Funcionario creado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para verificar la contraseña de un cliente
@app.post("/verify-client/")
async def verify_client(correo: str, contraseña: str):
    try:
        # Buscar el cliente por correo en la base de datos
        response = supabase.table("Clientes").select("*").eq("correo", correo).execute()

        # Verificar si el cliente existe
        if len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cliente = response.data[0]  # Obtener los datos del cliente
        hashed_password = cliente["contraseña"]  # La contraseña cifrada almacenada en la base de datos

        # Verificar si la contraseña es correcta
        if verify_password(contraseña, hashed_password):
            return {"message": "Contraseña correcta"}
        else:
            return {"message": "Contraseña incorrecta"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))