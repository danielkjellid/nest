from fastapi import FastAPI

from nest import config

app = FastAPI(title="Nest", docs_url="/docs")


@app.get("/")
async def root():
    return {"message": "Hello World", "DB": config.DATABASE_URL}
