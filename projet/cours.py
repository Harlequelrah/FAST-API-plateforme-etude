from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_cours=APIRouter(
    prefix='/cours',
    tags=['cours']
)


@app_cours.post("/cours/postcours", response_model=schemas.Cours)
def create_cours(cours: schemas.CoursCreate, db: Session = Depends(get_db)):
    return crud.create_cours(db=db, cours=cours)

@app_cours.get("/cours/getcours/{id_Cours}", response_model=schemas.Cours)
def read_cours(id_Cours: int, db: Session = Depends(get_db)):
    db_cours = crud.get_cours(db, id_Cours=id_Cours)
    if db_cours is None:
        raise HTTPException(status_code=404, detail='Cours non trouvé')
    return db_cours

@app_cours.get("/cours/getall",response_model=list[schemas.Cours])
def read_cours(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    cours=crud.get_all_cours(db,skip=skip,limit=limit)
    return cours

@app_cours.put("/cours/update/{id_Cours}", response_model=schemas.Cours)
def update_cours(id_Cours: int, cours_update: schemas.CoursUpdate, db: Session = Depends(get_db)):
    db_cours = crud.get_cours(db, id_Cours=id_Cours)
    if db_cours is None:
        raise HTTPException(status_code=404, detail='Cours non trouvé')

    # Mise à jour des champs modifiables
    db_cours.nom_Cours = cours_update.nom_Cours
    db_cours.libelle_Cours = cours_update.libelle_Cours
    db_cours.contenue_text = cours_update.contenue_text
    db_cours.contenue_binary = cours_update.contenue_binary

    db.commit()
    db.refresh(db_cours)
    return db_cours


@app_cours.delete("/cours/delete/{id_Cours}", response_model=schemas.Cours)
def delete_cours(id_Cours: int, db: Session = Depends(get_db)):
    return crud.delete_cours(db,id_Cours)
