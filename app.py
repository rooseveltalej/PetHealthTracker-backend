import bcrypt
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client


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


# Función para cifrar la contraseña
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.get("/")
def read_root():
    return {"status": "Corriendo como vaca lechera"}



# Ruta GET para verificar la conexión a la base de datos
@app.get("/check-table/")
async def check_db(tabla: str):
    try:
        # Realizar una consulta simple para obtener todos los registros de la tabla 'Citas'
        response = supabase.table(tabla).select("*").execute()
        print(response)

        return {"message": "Connected to the database", "data": response.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Ruta de ejemplo que inserta un registro en Supabase
@app.post("/add-pet/")
async def add_item(name: str, especie: str, raza: str, fecha_nacimiento: str, id_dueño: str):
    try:
        data = {
            "nombre_mascota": name,
            "especie": especie,
            "raza": raza,
            "fecha_nacimiento": fecha_nacimiento,
            "id_dueño": id_dueño
        }
        # Inserta el nuevo registro en la tabla 'items'
        response = supabase.table("Mascotas").insert(data).execute()

        # Verificar el estado de la respuesta
        print(response)

        return {"message": "Item added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Ruta post para Clientes
@app.post("/add-client/")
async def add_client(nombre: str, correo: str, contraseña: str):
    try:
        # Cifrar la contraseña antes de almacenarla
        hashed_password = hash_password(contraseña)
        
        data = {
            "nombre_usuario": nombre,
            "correo": correo,
            "contraseña": hashed_password  # Almacenar el hash en lugar de la contraseña en texto plano
        }

        # Inserta el nuevo registro en la tabla 'Clientes'
        response = supabase.table("Clientes").insert(data).execute()

        return {"message": "Client added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Ruta post para Citas
@app.post("/add-appointment/")
async def add_appointment(id_mascota: str, fecha_cita: str, id_veterinario: str, hora_cita: str):
    try:
        data = {
            "id_mascota": id_mascota,
            "fecha_cita": fecha_cita,
            "id_veterinario": id_veterinario,
            "hora_cita": hora_cita
        }

        # Inserta el nuevo registro en la tabla 'Citas'
        response = supabase.table("Citas").insert(data).execute()

        return {"message": "Appointment added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Ruta para verificar la contraseña de un cliente (ejemplo)
@app.post("/verify-client/")
async def verify_client(correo: str, contraseña: str):
    try:
        # Supongamos que obtienes el cliente desde la base de datos (sólo un ejemplo)
        response = supabase.table("Clientes").select("*").eq("correo", correo).execute()
        if len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cliente = response.data[0]
        hashed_password = cliente["contraseña"]

        # Verificar la contraseña
        if verify_password(contraseña, hashed_password):
            return {"message": "Contraseña correcta"}
        else:
            return {"message": "Contraseña incorrecta"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))