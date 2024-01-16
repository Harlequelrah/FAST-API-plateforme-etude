from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles  import StaticFiles
from mysqlapp.models import Etudiant
templates = Jinja2Templates(directory="PYTHON-PROJECT/projet/templates")


app_etudiant=APIRouter(
    prefix='/etudiants',
    tags=['etudiants']
)



@app_etudiant.get("/etudiants/getby-id/{id_Etud}",response_model=schemas.Etudiant,operation_id="get_etudiant")
def read_etudiant(id_Etud:int,db:Session=Depends(get_db)):
    return crud.get_etudiant(db,id_Etud)


@app_etudiant.get("/etudiants/getby-email/{email_Etud}",response_model=schemas.Etudiant)
def read_etudiant(email_Etud:str,db:Session=Depends(get_db)):
    return crud.get_etudiant_by_email(db,email_Etud)


@app_etudiant.get("/etudiants/getall",response_model=list[schemas.Etudiant])
def read_etudiants(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    etudiants=crud.get_etudiants(db,skip=skip,limit=limit)
    return etudiants

@app_etudiant.get("/etudiants/getcountetudiants")
def  count_etudiant(db:Session=Depends(get_db)):
     count = crud.get_count_etudiants(db)
     return {"nombred d ' etudiants":count}



@app_etudiant.put("/etudiants/update/{id_Etud}", response_model=schemas.Etudiant)
def update_etudiant(id_Etud: int, etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    return crud.update_etudiant(id_Etud,etudiant,db)



@app_etudiant.delete("/etudiants/delete/{id_Etud}", response_model=schemas.Etudiant)
def delete_etudiant(id_Etud: int, db: Session = Depends(get_db)):
    return crud.delete_etudiant(db=db, id_Etud=id_Etud)







@app_etudiant.get("/etudiants/create_by_form",response_class=HTMLResponse)
async def create_by_form(request: Request):
  return templates.TemplateResponse("create_etudiant.html", {"request":request})





@app_etudiant.post("/etudiants/submit",response_model=schemas.Etudiant)
async def submit(db:Session=Depends(get_db),nom:str=Form(...),prenom:str=Form(...),email:str=Form(...),password:str=Form(...),date_naissance:str=Form(...),universite_provenance:str=Form(...)):
 etudiant=Etudiant(nom_Etud=nom,prenom_Etud=prenom,mot_de_passe=password,email_Etud=email,date_Naissance=date_naissance,universite_Provenance=universite_provenance)
 db_etudiant=crud.get_etudiant_by_email(db,email)
 if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet Etudiant existe déja")
 return crud.create_etudiant(db=db,etudiant=etudiant)



@app_etudiant.post("/etudiants/create",response_model=schemas.Etudiant)
def create_etudiant(etudiant:schemas.EtudiantCreate,db:Session=Depends(get_db)):
    db_etudiant=crud.get_etudiant_by_email(db,email=etudiant.email_Etud)
    if db_etudiant:
        raise HTTPException(status_code=400,detail="Cet Etudiant existe déja")
    return crud.create_etudiant(db=db,etudiant=etudiant)


