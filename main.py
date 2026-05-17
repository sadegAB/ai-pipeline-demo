from fastapi import FastAPI
from config import settings
from middleware.cors import add_cors
from routers import health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

add_cors(app)

# ── Routers ──
app.include_router(health.router)

# ── Add new routers here ──
# from routers import books
# app.include_router(books.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}
