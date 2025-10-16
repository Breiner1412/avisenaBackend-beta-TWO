from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import fincas, users, aislamientos, categorias_inventario, detalle_salvamento, detalle_huevos, galpones, incidentes_gallina, incidentes_generales, ingreso_gallinas, inventario_finca, metodo_pago, produccion_huevos, registro_sensores, salvamento, sensores, stock, tareas, tipo_gallinas, tipo_huevos, tipo_sensores, ventas
from app.router import auth
app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(fincas.router, prefix="/fincas", tags=["fincas"])
app.include_router(aislamientos.router, prefix="/aislamientos", tags=["aislamientos"])
app.include_router(categorias_inventario.router, prefix="/categorias-inventario", tags=["categorias-inventario"])
app.include_router(detalle_salvamento.router, prefix="/detalle-salvamento", tags=["detalle-salvamento"])
app.include_router(detalle_huevos.router, prefix="/detalle-huevos", tags=["detalle-huevos"])
app.include_router(galpones.router, prefix="/galpones", tags=["galpones"])
app.include_router(incidentes_gallina.router, prefix="/incidentes-gallina", tags=["incidentes-gallina"])
app.include_router(incidentes_generales.router, prefix="/incidentes-generales", tags=["incidentes-generales"])
app.include_router(ingreso_gallinas.router, prefix="/ingreso-gallinas", tags=["ingreso-gallinas"])
app.include_router(inventario_finca.router, prefix="/inventario-finca", tags=["inventario-finca"])
app.include_router(metodo_pago.router, prefix="/metodo-pago", tags=["metodo-pago"])
app.include_router(produccion_huevos.router, prefix="/produccion-huevos", tags=["produccion-huevos"])
app.include_router(registro_sensores.router, prefix="/registro-sensores", tags=["registro-sensores"])
app.include_router(salvamento.router, prefix="/salvamento", tags=["salvamento"])
app.include_router(sensores.router, prefix="/sensores", tags=["sensores"])
app.include_router(stock.router, prefix="/stock", tags=["stock"])
app.include_router(tareas.router, prefix="/tareas", tags=["tareas"])
app.include_router(tipo_gallinas.router, prefix="/tipo-gallinas", tags=["tipo-gallinas"])
app.include_router(tipo_huevos.router, prefix="/tipo-huevos", tags=["tipo-huevos"])
app.include_router(tipo_sensores.router, prefix="/tipo-sensores", tags=["tipo-sensores"])
app.include_router(ventas.router, prefix="/ventas", tags=["ventas"])



# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
                "autor": "ADSO 2925889"
            }

