from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_contenir=APIRouter(
    prefix='/contenir',
    tags=['contenir']
)
@app_contenir.put("/contenir/{id_Contenir}", response_model=schemas.Contenir)
def update_contenir(id_Contenir: int, contenir: schemas.ContenirCreate, db: Session = Depends(get_db)):
    return crud.update_contenir(db=db, id_Contenir=id_Contenir, contenir=contenir)

@app_contenir.delete("/contenir/{id_Contenir}", response_model=schemas.Contenir)
def delete_contenir(id_Contenir: int, db: Session = Depends(get_db)):
    return crud.delete_contenir(db=db, id_Contenir=id_Contenir)
