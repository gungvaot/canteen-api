from fastapi import FastAPI

from app.routers import menu

app = FastAPI(title="Canteen API", version="1.0.0",
              description="API thực đơn căng tin trường")
app.include_router(menu.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
