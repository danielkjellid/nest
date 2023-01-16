from fastapi import FastAPI

from nest.config import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World", "DB": settings.database_url}
