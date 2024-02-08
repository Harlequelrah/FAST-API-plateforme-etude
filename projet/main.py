# from fastapi import FastAPI
# import uvicorn
# from user import *
from projet.mysqlapp import crud, models, schemas
# app=FastAPI()
from projet.mysqlapp.database import get_db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import date
# from . import crud, models, schemas
from projet.mysqlapp.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
import uvicorn
app = FastAPI()
from projet.enseigner import *
from projet.contenir import *
from projet.enseigner import *
from projet.etudiant import *
from projet.cours import *
from projet.professeur import *
from projet.module import *
from projet.inscription import *
models.Base.metadata.create_all(bind=engine)
app.include_router(app_etudiant)
app.include_router(app_cours)
app.include_router(app_professeur)
app.include_router(app_module)
app.include_router(app_enseigner)
app.include_router(app_contenir)
app.include_router(app_inscription)

app.mount("/static", StaticFiles(directory="PYTHON-PROJECT/projet/static"), name="static")
if __name__=="__main__":
   uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
# Dependency
