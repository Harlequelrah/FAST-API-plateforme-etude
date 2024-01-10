from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_professeur=APIRouter(
    prefix='/professeurs',
    tags=['professeurs']
)

@app_professeur.put("/professeurs/{id_Prof}", response_model=schemas.Professeur)
def update_professeur(id_Prof: int, professeur: schemas.ProfesseurCreate, db: Session = Depends(get_db)):
    return crud.update_professeur(db=db, id_Prof=id_Prof, professeur=professeur)

@app_professeur.delete("/professeurs/{id_Prof}", response_model=schemas.Professeur)
def delete_professeur(id_Prof: int, db: Session = Depends(get_db)):
    return crud.delete_professeur(db=db, id_Prof=id_Prof)
