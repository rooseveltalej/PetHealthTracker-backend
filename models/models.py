from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Mascota(BaseModel):
    id: Optional[int]
    nombre: str
    edad: int
    especie: str
    raza: str
    cliente_id: int
    image_url: Optional[str]

class Cliente(BaseModel):
    id: Optional[int]
    nombre_usuario: str
    correo: str
    contraseña: str

class Cita(BaseModel):
    id: Optional[int]
    id_mascota: int
    fecha_cita: datetime
    motivo: str
    id_veterinario: int

class Diagnostico(BaseModel):
    id: Optional[int]
    id_cita: int
    descripcion: str
    resultado: str

class Funcionario(BaseModel):
    id: Optional[int]
    nombre: str
    correo: str
    contraseña: str
    puesto: str

class LoginRequest(BaseModel):
    correo: str
    contraseña: str
    role: str  # Puede ser 'cliente' o 'funcionario'

class CompleteCitaData(BaseModel):
    tipo: str
    motivo: str
    resultado: str
