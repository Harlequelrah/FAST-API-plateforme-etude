from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles  import StaticFiles
from mysqlapp.models import Etudiant

app_etudiant=APIRouter(
    prefix='/etudiants',
    tags=['etudiants']
)

@app_etudiant.get("/etudiants/get/{id_Etud}",response_model=schemas.Etudiant,operation_id="get_etudiant")
def read_etudiant(id_Etudiant:int,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant(db,id_Etudiant)
    if db_etudiant is None :
        raise HTTPException(status_code=404,detail ='Etudiant non trouvé')
    return db_etudiant

@app_etudiant.get("/etudiants/get_all",response_model=list[schemas.Etudiant])
def read_etudiants(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    etudiants=crud.get_etudiants(db,skip=skip,limit=limit)
    return etudiants





@app_etudiant.put("/etudiants/update/{id_Etud}", response_model=schemas.Etudiant)
def update_etudiant(id_Etud: int, etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, id_Etud)

    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')

    # Vérifie s'il y a des champs de mise à jour dans etudiant
    if etudiant.nom_Etud is not None:
        db_etudiant.nom_Etud = etudiant.nom_Etud
    if etudiant.prenom_Etud is not None:
        db_etudiant.prenom_Etud = etudiant.prenom_Etud
    if etudiant.email_Etud is not None:
        db_etudiant.email_Etud = etudiant.email_Etud
    if etudiant.date_Naissance is not None:
        db_etudiant.date_Naissance = etudiant.date_Naissance
    if etudiant.universite_Provenance is not None:
        db_etudiant.universite_Provenance = etudiant.universite_Provenance
    if etudiant.mot_de_passe is not None:
        db_etudiant.mot_de_passe = etudiant.mot_de_passe

    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant




@app_etudiant.delete("/etudiants/delete/{id_Etud}", response_model=schemas.Etudiant)
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, id_Etud)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')

    crud.delete_etudiant(db=db, id_Etud=id_Etud)

    return db_etudiant





templates = Jinja2Templates(directory="PYTHON-PROJECT/projet/templates")

@app_etudiant.get("/etudiants/create_by_form",response_class=HTMLResponse)
async def create_by_form(request: Request):
  return templates.TemplateResponse("create_etudiant.html", {"request":request})


@app_etudiant.post("/etudiants/submit",response_model=schemas.Etudiant)
async def submit(db:Session=Depends(get_db),nom:str=Form(...),prenom:str=Form(...),email:str=Form(...),password:str=Form(...),date_naissance:str=Form(...),universite_provenance:str=Form(...)):
 etudiant=Etudiant(nom_Etud=nom,prenom_Etud=prenom,mot_de_passe=password,email_Etud=email,date_Naissance=date_naissance,universite_Provenance=universite_provenance)
 db_etudiant=crud.get_etudiant_by_email(db,email)
 if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet email existe déja")
 return crud.create_etudiant(db=db,etudiant=etudiant)



@app_etudiant.post("/etudiants/create",response_model=schemas.Etudiant)
def create_etudiant(etudiant:schemas.EtudiantCreate,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant_by_email(db,email=etudiant.email_Etud)
    if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet email existe déja")
    return crud.create_etudiant(db=db,etudiant=etudiant)
