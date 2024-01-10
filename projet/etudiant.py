from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_etudiant=APIRouter(
    prefix='/etudiants',
    tags=['etudiants']
)


@app_etudiant.post("/etudiants/",response_model=schemas.Etudiant)
def create_etudiant(etudiant:schemas.EtudiantCreate,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant_by_email(db,email=etudiant.email_Etud)
    if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet email existe déja")
    return crud.create_etudiant(db=db,etudiant=etudiant)

@app_etudiant.get("/etudiants/",response_model=list[schemas.Etudiant])
def read_etudiants(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    etudiants=crud.get_etudiants(db,skip=skip,limit=limit)
    return etudiants

@app_etudiant.put("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
def update_etudiant(id_Etud: int, etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    return crud.update_etudiant(db=db, id_Etud=id_Etud, etudiant=etudiant)

@app_etudiant.delete("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    return crud.delete_etudiant(db=db, id_Etud=id_Etud)


@app_etudiant.get("/etudiants/{id_Etud}",response_model=schemas.Etudiant)
def read_etudiant(id_Etudiant:int,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant(db,id_Etudiant=id_Etudiant)
    if db_etudiant is None :
        raise HTTPException(status_code=404,detail ='Etudiant non trouvé')
    return db_etudiant

@app_etudiant.put("/etudiants/{id_Etud}", response_model=schemas.Etudiant,operation_id="update_etudiant")
def update_etudiant(id_Etud: int, etudiant_update: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, id_Etud)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')

    # Mise à jour des champs modifiables
    db_etudiant.nom_Etud = etudiant_update.nom_Etud
    db_etudiant.prenom_Etud = etudiant_update.prenom_Etud
    db_etudiant.email_Etud = etudiant_update.email_Etud
    db_etudiant.date_Naissance = etudiant_update.date_Naissance
    db_etudiant.universite_Provenance = etudiant_update.universite_Provenance
    db_etudiant.mot_de_passe = etudiant_update.mot_de_passe

    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

@app_etudiant.delete("/etudiants/{id_Etud}", response_model=schemas.Etudiant,operation_id="delete_etudiant")
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, id_Etud)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')

    db.delete(db_etudiant)
    db.commit()

    return db_etudiant
