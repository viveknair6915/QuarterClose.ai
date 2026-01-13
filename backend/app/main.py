from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import data, reports, admin

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="QuarterClose.ai", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(data.router)
app.include_router(reports.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "QuarterClose.ai API is running"}
