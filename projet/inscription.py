from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_inscription=APIRouter(
    prefix='/inscriptions',
    tags=['inscriptions']
)
@app_inscription.post("/inscriptions/", response_model=schemas.Inscription)
def create_inscription(inscription: schemas.InscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_inscription(db=db, inscription=inscription)

@app_inscription.get("/inscriptions/{id_Etud}/{id_Cours}", response_model=schemas.Inscription)
def read_inscription(id_Etud: int, id_Cours: int, db: Session = Depends(get_db)):
    db_inscription = crud.get_inscription(db, id_Etud=id_Etud, id_Cours=id_Cours)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail='Inscription non trouvée')
    return db_inscription

@app_inscription.put("/inscriptions/{id_Etud}/{id_Cours}", response_model=schemas.Inscription)
def update_inscription(id_Etud: int, id_Cours: int, inscription_update: schemas.InscriptionCreate, db: Session = Depends(get_db)):
    db_inscription = crud.get_inscription(db, id_Etud=id_Etud, id_Cours=id_Cours)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail='Inscription non trouvée')

    # Mise à jour des champs modifiables
    db_inscription.id_Session = inscription_update.id_Session
    db_inscription.date_Inscription = inscription_update.date_Inscription
    db_inscription.status = inscription_update.status

    db.commit()
    db.refresh(db_inscription)
    return db_inscription