from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mysqlapp.models import Professeur
app_professeur=APIRouter(
    prefix='/professeurs',
    tags=['professeurs']
)


templates = Jinja2Templates(directory="PYTHON-PROJECT/projet/templates")

@app_professeur.post("/", response_model=schemas.Professeur)
def create_professeur(professeur: schemas.ProfesseurCreate, db: Session = Depends(get_db)):
    db_professeur=crud.get_professeur_by_email(db,email=professeur.email_Prof)
    if db_professeur :raise HTTPException(status_code=400,detail="Ce Professeur existe déja")
    return crud.create_professeur(db=db, professeur=professeur)

# Endpoint pour récupérer un professeur par son identifiant
@app_professeur.get("/professeurs/getby-id{id_Prof}", response_model=schemas.Professeur)
def read_professeur(id_Prof: int, db: Session = Depends(get_db)):
   return crud.get_professeur(db=db, id_Prof=id_Prof)

@app_professeur.get("/professeurs/getby-email/{email_Prof}",response_model=schemas.Professeur)
def read_professeur(email_Prof:str,db:Session=Depends(get_db)):
    return crud.get_professeur_by_email(db,email_Prof)


@app_professeur.get("/professeurs/getall", response_model=list[schemas.Professeur])
def read_professeurs(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    professeurs=crud.get_professeurs(db,skip=skip,limit=limit)
    return professeurs

@app_professeur.put("/professeurs/update/{id_Prof}", response_model=schemas.Professeur)
def update_professeur(id_Prof: int, professeur: schemas.ProfesseurCreate, db: Session = Depends(get_db)):
    return crud.update_professeur(db=db, id_Prof=id_Prof, professeur=professeur)

@app_professeur.delete("/professeurs/delete/{id_Prof}", response_model=schemas.Professeur)
def delete_professeur(id_Prof: int, db: Session = Depends(get_db)):
    return crud.delete_professeur(db=db, id_Prof=id_Prof)

@app_professeur.get("/professeurs/getcountprofesseurs")
def  count_professeur(db:Session=Depends(get_db)):
     count = crud.get_count_professeurs(db)
     return {"nombred de professeurs":count}

@app_professeur.get("/professeurs/create_by_form",response_class=HTMLResponse)
async def create_by_form(request: Request):
  return templates.TemplateResponse("create_professeur.html", {"request":request})

@app_professeur.post("/professeurs/submit",response_model=schemas.Professeur)
async def submit(db:Session=Depends(get_db),nom:str=Form(...),prenom:str=Form(...),email:str=Form(...),password:str=Form(...)):
 professeur=Professeur(nom_Prof=nom,prenom_Prof=prenom,password_Prof=password,email_Prof=email)
 db_professeur=crud.get_professeur_by_email(db,email)
 if db_professeur:
        raise HTTPException(status_code=400,detail="Ce professeur déja")
 return crud.create_professeur(db=db,professeur=professeur)
