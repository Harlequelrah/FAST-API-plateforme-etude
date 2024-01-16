from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_contenir=APIRouter(
    prefix='/contenir',
    tags=['contenir']
)
@app_contenir.put("/contenir/update", response_model=schemas.Contenir)
def update_contenir(contenir: schemas.ContenirCreate, db: Session = Depends(get_db)):
    # Vérifier si la relation "Contenir" existe
    db_contenir = crud.get_contenir_by_ids(db, contenir.id_Cours, contenir.id_Module)

    if db_contenir is None:
        raise HTTPException(status_code=404, detail="Relation Contenir non trouvée")

    # Mettre à jour la relation
    for key, value in contenir.dict().items():
        setattr(db_contenir, key, value)

    db.commit()
    db.refresh(db_contenir)

    return db_contenir



@app_contenir.post("/contenir/", response_model=schemas.Contenir)
def create_contenir(contenir: schemas.ContenirCreate, db: Session = Depends(get_db)):
    # Vérifier si le cours et le module existent avant de créer la relation
    db_cours = crud.get_cours(db, contenir.id_Cours)
    db_module = crud.get_module(db, contenir.id_Module)

    if db_cours is None or db_module is None:
        raise HTTPException(status_code=404, detail="Cours ou module non trouvé")

    # Créer la relation
    db_contenir = models.Contenir(
        id_Cours=contenir.id_Cours,
        id_Module=contenir.id_Module
    )

    db.add(db_contenir)
    db.commit()
    db.refresh(db_contenir)

    return

