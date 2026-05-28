from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jackdaw.server.routes import test_data, health, log
from jackdaw.config import ConfigManager

ConfigManager.ensure_config_exists()

app = FastAPI(title="Jackdaw Local Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_data.router)
app.include_router(health.router)
app.include_router(log.router)