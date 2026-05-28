from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jackdaw.server.routes import test_data

app = FastAPI(title="Jackdaw Local Server")

# Allow the Next.js frontend (running on port 3000 during dev) to hit this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your new route
app.include_router(test_data.router)

@app.get("/api/health")
def health_check():
    return {"status": "Jackdaw is sailing"}