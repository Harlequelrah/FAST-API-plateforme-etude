from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_enseigner=APIRouter(
    prefix='/enseigner',
    tags=['enseigner']
)

@app_enseigner.put("/enseigner/{id_Enseigner}", response_model=schemas.Enseigner)
def update_enseigner(id_Enseigner: int, enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):
    return crud.update_enseigner(db=db, id_Enseigner=id_Enseigner, enseigner=enseigner)

@app_enseigner.delete("/enseigner/{id_Enseigner}", response_model=schemas.Enseigner)
def delete_enseigner(id_Enseigner: int, db: Session = Depends(get_db)):
    return crud.delete_enseigner(db=db, id_Enseigner=id_Enseigner)
