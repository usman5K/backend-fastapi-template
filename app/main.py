from fastapi import FastAPI, status

from app.api import v1_router

app = FastAPI(
    title="Backend FastAPI Template",
    version="0.1.0",
    description="A scalable FastAPI backend template",
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
def read_root():
    return {"message": "Welcome to the Backend FastAPI Template!"}


app.include_router(v1_router.routes, prefix="/api")
