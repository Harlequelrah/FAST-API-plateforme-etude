from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from . import crud, models, schemas
from .database import SessionLocal, engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# if __name__=="__main__":
#    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/etudiants/",response_model=schemas.Etudiant)
def create_etudiant(etudiant:schemas.EtudiantCreate,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant_by_email(db,email=etudiant.email_Etud)
    if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet email existe déja")
    return crud.create_etudiant(db=db,etudiant=etudiant)

@app.get("/etudiants/",response_model=list[schemas.Etudiant])
def read_etudiants(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    etudiants=crud.get_etudiants(db,skip=skip,limit=limit)
    return etudiants

@app.put("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
def update_etudiant(id_Etud: int, etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    return crud.update_etudiant(db=db, id_Etud=id_Etud, etudiant=etudiant)

@app.delete("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    return crud.delete_etudiant(db=db, id_Etud=id_Etud)


@app.get("/etudiants/{id_Etud}",response_model=schemas.Etudiant)
def read_etudiant(id_Etudiant:int,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant(db,id_Etudiant=id_Etudiant)
    if db_etudiant is None :
        raise HTTPException(status_code=404,detail ='Etudiant non trouvé')
    return db_etudiant

@app.put("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
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

@app.delete("/etudiants/{id_Etud}", response_model=schemas.Etudiant)
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, id_Etud)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')

    db.delete(db_etudiant)
    db.commit()

    return db_etudiant

@app.post("/cours/", response_model=schemas.Cours)
def create_cours(cours: schemas.CoursCreate, db: Session = Depends(get_db)):
    return crud.create_cours(db=db, cours=cours)

@app.get("/cours/{id_Cours}", response_model=schemas.Cours)
def read_cours(id_Cours: int, db: Session = Depends(get_db)):
    db_cours = crud.get_cours(db, id_Cours=id_Cours)
    if db_cours is None:
        raise HTTPException(status_code=404, detail='Cours non trouvé')
    return db_cours

@app.put("/cours/{id_Cours}", response_model=schemas.Cours)
def update_cours(id_Cours: int, cours: schemas.CoursCreate, db: Session = Depends(get_db)):
    return crud.update_cours(db=db, id_Cours=id_Cours, cours=cours)

@app.delete("/cours/{id_Cours}", response_model=schemas.Cours)
def delete_cours(id_Cours: int, db: Session = Depends(get_db)):
    return crud.delete_cours(db=db, id_Cours=id_Cours)

@app.put("/cours/{id_Cours}", response_model=schemas.Cours)
def update_cours(id_Cours: int, cours_update: schemas.CoursCreate, db: Session = Depends(get_db)):
    db_cours = crud.get_cours(db, id_Cours=id_Cours)
    if db_cours is None:
        raise HTTPException(status_code=404, detail='Cours non trouvé')

    # Mise à jour des champs modifiables
    db_cours.nom_Cours = cours_update.nom_Cours
    db_cours.libelle_Cours = cours_update.libelle_Cours
    db_cours.contenue = cours_update.contenue

    db.commit()
    db.refresh(db_cours)
    return db_cours

@app.delete("/cours/{id_Cours}", response_model=schemas.Cours)
def delete_cours(id_Cours: int, db: Session = Depends(get_db)):
    db_cours = crud.get_cours(db, id_Cours=id_Cours)
    if db_cours is None:
        raise HTTPException(status_code=404, detail='Cours non trouvé')

    db.delete(db_cours)
    db.commit()

    return db_cours


@app.post("/inscriptions/", response_model=schemas.Inscription)
def create_inscription(inscription: schemas.InscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_inscription(db=db, inscription=inscription)

@app.get("/inscriptions/{id_Etud}/{id_Cours}", response_model=schemas.Inscription)
def read_inscription(id_Etud: int, id_Cours: int, db: Session = Depends(get_db)):
    db_inscription = crud.get_inscription(db, id_Etud=id_Etud, id_Cours=id_Cours)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail='Inscription non trouvée')
    return db_inscription

@app.put("/inscriptions/{id_Etud}/{id_Cours}", response_model=schemas.Inscription)
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

@app.delete("/inscriptions/{id_Etud}/{id_Cours}", response_model=schemas.Inscription)
def delete_inscription(id_Etud: int, id_Cours: int, db: Session = Depends(get_db)):
    db_inscription = crud.get_inscription(db, id_Etud=id_Etud, id_Cours=id_Cours)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail='Inscription non trouvée')

    db.delete(db_inscription)
    db.commit()

    return db_inscription

@app.get("/inscriptions/", response_model=list[schemas.Inscription])
def read_all_inscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inscriptions = crud.get_all_inscriptions(db, skip=skip, limit=limit)
    return inscriptions

@app.get("/inscriptions/date/{date}", response_model=list[schemas.Inscription])
def read_inscriptions_by_date(date: date, db: Session = Depends(get_db)):
    inscriptions = crud.get_inscriptions_by_date(db, date=date)
    return inscriptions

@app.get("/inscriptions/etudiant/{id_Etud}", response_model=list[schemas.Inscription])
def read_inscriptions_by_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    inscriptions = crud.get_inscriptions_by_etudiant(db, id_Etud=id_Etud)
    return inscriptions

@app.get("/inscriptions/cours/{id_Cours}", response_model=list[schemas.Inscription])
def read_inscriptions_by_cours(id_Cours: int, db: Session = Depends(get_db)):
    inscriptions = crud.get_inscriptions_by_cours(db, id_Cours=id_Cours)
    return inscriptions

@app.put("/professeurs/{id_Prof}", response_model=schemas.Professeur)
def update_professeur(id_Prof: int, professeur: schemas.ProfesseurCreate, db: Session = Depends(get_db)):
    return crud.update_professeur(db=db, id_Prof=id_Prof, professeur=professeur)

@app.delete("/professeurs/{id_Prof}", response_model=schemas.Professeur)
def delete_professeur(id_Prof: int, db: Session = Depends(get_db)):
    return crud.delete_professeur(db=db, id_Prof=id_Prof)



@app.put("/enseigner/{id_Enseigner}", response_model=schemas.Enseigner)
def update_enseigner(id_Enseigner: int, enseigner: schemas.EnseignerCreate, db: Session = Depends(get_db)):
    return crud.update_enseigner(db=db, id_Enseigner=id_Enseigner, enseigner=enseigner)

@app.delete("/enseigner/{id_Enseigner}", response_model=schemas.Enseigner)
def delete_enseigner(id_Enseigner: int, db: Session = Depends(get_db)):
    return crud.delete_enseigner(db=db, id_Enseigner=id_Enseigner)



@app.put("/modules/{id_Module}", response_model=schemas.Module)
def update_module(id_Module: int, module: schemas.ModuleCreate, db: Session = Depends(get_db)):
    return crud.update_module(db=db, id_Module=id_Module, module=module)

@app.delete("/modules/{id_Module}", response_model=schemas.Module)
def delete_module(id_Module: int, db: Session = Depends(get_db)):
    return crud.delete_module(db=db, id_Module=id_Module)



@app.put("/contenir/{id_Contenir}", response_model=schemas.Contenir)
def update_contenir(id_Contenir: int, contenir: schemas.ContenirCreate, db: Session = Depends(get_db)):
    return crud.update_contenir(db=db, id_Contenir=id_Contenir, contenir=contenir)

@app.delete("/contenir/{id_Contenir}", response_model=schemas.Contenir)
def delete_contenir(id_Contenir: int, db: Session = Depends(get_db)):
    return crud.delete_contenir(db=db, id_Contenir=id_Contenir)
