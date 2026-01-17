from fastapi import FastAPI
from .db import engine
from . import models
from .routes import auth, users, parks, species, recommendations

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TABI3A API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(parks.router)
app.include_router(species.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {"message": "Welcome to TABI3A"}
