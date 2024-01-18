from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_enseigner=APIRouter(
    prefix='/enseigner',
    tags=['enseigner']
)


@app_enseigner.get("/enseigner/{id_Prof}/{id_Cours}", response_model=schemas.Enseigner)
def read_enseigner(id_Prof: int, id_Cours: int, db: Session = Depends(get_db)):
    db_enseigner = crud.get_enseigner_by_ids(db, id_Prof, id_Cours)
    if db_enseigner is None:
        raise HTTPException(status_code=404, detail="Relation d'enseignement non trouvée")
    return db_enseigner


@app_enseigner.put("/enseigner/{id_Prof}/{id_Cours}", response_model=schemas.Enseigner)
def update_enseigner_route(
    id_Prof: int, id_Cours: int, enseigner_update: schemas.EnseignerCreate, db: Session = Depends(get_db)
):
    db_enseigner = crud.get_enseigner_by_ids(db, id_Prof, id_Cours)
    if db_enseigner is None:
        raise HTTPException(status_code=404, detail="Relation d'enseignement non trouvée")


    db_enseigner.session_Debut = enseigner_update.session_Debut
    db_enseigner.session_Fin = enseigner_update.session_Fin
    db_enseigner.volume_Horaire = enseigner_update.volume_Horaire

    db.commit()
    db.refresh(db_enseigner)
    return db_enseigner


@app_enseigner.delete("/enseigner/{id_Prof}/{id_Cours}", response_model=schemas.Enseigner)
def delete_enseigner_route(id_Prof: int, id_Cours: int, db: Session = Depends(get_db)):
    db_enseigner = crud.get_enseigner_by_ids(db, id_Prof, id_Cours)
    if db_enseigner is None:
        raise HTTPException(status_code=404, detail="Relation d'enseignement non trouvée")

    db_enseigner = crud.delete_enseigner(db, id_Prof, id_Cours)
    return db_enseigner


@app_enseigner.post("/enseigner/create", response_model=schemas.Enseigner)
def create_enseigner_route(enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):

    db_cours = crud.get_cours(db, enseigner.id_Cours)
    db_prof = crud.get_prof(db, enseigner.id_Prof)

    if db_cours is None or db_prof is None:
        raise HTTPException(status_code=404, detail="Cours ou professeur non trouvé")


    db_enseigner = crud.create_enseigner(db=db, enseigner=enseigner)

    return db_enseigner
