from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_contenir=APIRouter(
    prefix='/contenir',
    tags=['contenir']
)

@app_contenir.get("/contenir/read/{id_Module}/{id_Cours}", response_model=schemas.Contenir)
def read_contenir(id_Module: int, id_Cours: int, db: Session = Depends(get_db)):
     db_cours = crud.get_cours(db, id_Cours)
     db_module = crud.get_module(db, id_Module)
     if db_cours is None or db_module is None:
        raise HTTPException(status_code=404, detail="Cours ou module non trouvé")

     return crud.get_contenir_by_ids(db, id_Module, id_Cours)

@app_contenir.put("/contenir/update/{id_Module}/{id_Cours}", response_model=schemas.Contenir)
def update_contenir(id_Module: int, id_Cours: int, db: Session = Depends(get_db)):
    # Vérifier si le cours et le module existent avant de mettre à jour la relation
    db_cours = crud.get_cours(db, id_Cours)
    db_module = crud.get_module(db, id_Module)

    if db_cours is None or db_module is None:
        raise HTTPException(status_code=404, detail="Cours ou module non trouvé")

    # Vérifier si la relation existe
    db_contenir = crud.get_contenir_by_ids(db, id_Module, id_Cours)

    if db_contenir is None:
        raise HTTPException(status_code=404, detail="Relation contenir non trouvée")

    # Mise à jour des champs si nécessaire
    # ...

    db.commit()
    db.refresh(db_contenir)

    return {"message": "Association contenir mise à jour avec succès", "contenir": db_contenir}



@app_contenir.delete("/contenir/delete/{id_Module}/{id_Cours}")
def delete_contenir(id_Module: int, id_Cours: int, db: Session = Depends(get_db)):
    # Vérifier si le cours et le module existent avant de supprimer la relation
    db_cours = crud.get_cours(db, id_Cours)
    db_module = crud.get_module(db, id_Module)

    if db_cours is None or db_module is None:
        raise HTTPException(status_code=404, detail="Cours ou module non trouvé")

    # Vérifier si la relation existe
    db_contenir = crud.get_contenir_by_ids(db, id_Module, id_Cours)

    if db_contenir is None:
        raise HTTPException(status_code=404, detail="Relation contenir non trouvée")

    # Supprimer la relation
    db.delete(db_contenir)
    db.commit()

    return {"message": "Association contenir supprimée avec succès"}

@app_contenir.post("/contenir/create", response_model=schemas.Contenir)
def create_contenir(id_Module: int, id_Cours: int,db: Session = Depends(get_db)):
    # Vérifier si le cours et le module existent avant de créer la relation
    db_cours = crud.get_cours(db,id_Cours)
    db_module = crud.get_module(db, id_Module)

    if db_cours is None or db_module is None:
        raise HTTPException(status_code=404, detail="Cours ou module non trouvé")

    # Créer la relation
    db_contenir = models.Contenir(
        id_Cours=id_Cours,
        id_Module=id_Module
    )

    db.add(db_contenir)
    db.commit()
    db.refresh(db_contenir)

    return  {"message": "Association contenir ajoutée avec succès"}

