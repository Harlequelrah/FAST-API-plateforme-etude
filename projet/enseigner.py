from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_enseigner=APIRouter(
    prefix='/enseigner',
    tags=['enseigner']
)

# @app_enseigner.put("/enseigner/update", response_model=schemas.Enseigner)
# def update_enseigner(id_Enseigner: int, enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):
#     return crud.update_enseigner(db=db, id_Enseigner=id_Enseigner, enseigner=enseigner)


@app_enseigner.put("/enseigner/update", response_model=schemas.Enseigner)
def update_enseigner(enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):
    # Vérifier si la relation "enseigner" existe
    db_enseigner = crud.get_enseigner_by_ids(db, enseigner.id_Prof, enseigner.id_Cours)

    if db_enseigner is None:
        raise HTTPException(status_code=404, detail="Relation enseigner non trouvée")

    # Mettre à jour la relation
    for key, value in enseigner.dict().items():
        setattr(db_enseigner, key, value)

    db.commit()
    db.refresh(db_enseigner)

    return db_enseigner



@app_enseigner.post("/enseigner/", response_model=schemas.Enseigner)
def create_enseigner(enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):
    # Vérifier si le cours et le module existent avant de créer la relation
    db_professeur = crud.get_professeur(db, enseigner.id_Prof)
    db_cours = crud.get_cours(db, enseigner.id_Cours)

    if db_cours is None or db_professeur is None:
        raise HTTPException(status_code=404, detail="professeur ou cours non trouvé")

    # Créer la relation
    db_enseigner = models.enseigner(
        id_Cours=enseigner.id_Cours,
        id_Prof=enseigner.id_Prof
    )

    db.add(db_enseigner)
    db.commit()
    db.refresh(db_enseigner)

    return

