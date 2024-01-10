from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_module=APIRouter(
    prefix='/module',
    tags=['module']
)

@app_module.put("/modules/{id_Module}", response_model=schemas.Module)
def update_module(id_Module: int, module: schemas.ModuleCreate, db: Session = Depends(get_db)):
    return crud.update_module(db=db, id_Module=id_Module, module=module)

@app_module.delete("/modules/{id_Module}", response_model=schemas.Module)
def delete_module(id_Module: int, db: Session = Depends(get_db)):
    return crud.delete_module(db=db, id_Module=id_Module)
