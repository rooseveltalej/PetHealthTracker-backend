from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Mascota(BaseModel):
    id: Optional[int]
    nombre_mascota: str
    especie: str
    raza: str
    fecha_nacimiento: str
    id_dueño: int
    image_url: Optional[str]

class Cliente(BaseModel):
    id: Optional[int]
    nombre_usuario: str
    correo: str
    contraseña: str

class Cita(BaseModel):
    id_mascota: int
    fecha_cita: str
    id_veterinario: int
    hora_cita: str

class Diagnostico(BaseModel):
    id: Optional[int]
    id_cita: int
    descripcion: str
    resultado: str

class Funcionario(BaseModel):
    nombre: str
    puesto: str = Field(..., min_length=1, description="El puesto es obligatorio")
    correo: str
    contraseña: str

    class Config:
        fields = {'nombre': 'nombre'}

class LoginRequest(BaseModel):
    correo: str
    contraseña: str
    role: str  # Puede ser 'cliente' o 'funcionario'

class CompleteCitaData(BaseModel):
    tipo: str
    motivo: str
    resultado: str
