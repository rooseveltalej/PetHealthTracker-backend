# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, mascotas, clientes, citas, funcionarios, vacunas, diagnosticos, upload

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto según tus necesidades de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(mascotas.router)
app.include_router(clientes.router)
app.include_router(citas.router)
app.include_router(funcionarios.router)
app.include_router(vacunas.router)
app.include_router(diagnosticos.router)
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}
