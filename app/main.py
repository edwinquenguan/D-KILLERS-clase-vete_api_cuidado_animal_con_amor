from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from app.core.database import get_connection
from app.core.redis import close_redis, init_redis
from app.features.auth.routes import auth_routes
from app.features.users.routes import users_routes
from app.features.owners.routes import owners_routes
from app.features.species.routes import species_routes
from app.features.breeds.routes import breeds_routes
from app.features.pets.routes import pets_routes
from app.features.appointments.routes import appointments_routes
from app.features.consultations.routes import consultations_routes
from app.features.vaccines.routes import vaccines_routes
from app.features.vaccinations.routes import vaccinations_routes
from app.features.medications.routes import medications_routes
from app.features.prescriptions.routes import prescriptions_routes
from app.features.dashboard.routes import dashboard_routes
from app.features.reports.routes import reports_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis(app)
    await FastAPILimiter.init(redis)
    yield
    await close_redis()


app = FastAPI(
    title="Cuidado Animal con Amor - API",
    description="API REST para la clínica veterinaria Cuidado Animal con Amor",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping-db")
def ping_db():
    connection = get_connection()
    if connection:
        connection.close()
        return {"status": "Conexión exitosa a la base de datos"}
    return {"status": "Error al conectar con la base de datos"}


@app.get("/")
def root():
    return {"message": "Cuidado Animal con Amor - API funcionando"}


app.include_router(auth_routes.router)
app.include_router(users_routes.router)
app.include_router(owners_routes.router)
app.include_router(species_routes.router)
app.include_router(breeds_routes.router)
app.include_router(pets_routes.router)
app.include_router(appointments_routes.router)
app.include_router(consultations_routes.router)
app.include_router(vaccines_routes.router)
app.include_router(vaccinations_routes.router)
app.include_router(medications_routes.router)
app.include_router(prescriptions_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(reports_routes.router)
