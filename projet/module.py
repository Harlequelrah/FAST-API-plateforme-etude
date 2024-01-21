from mysqlapp import crud,schemas,models
from sqlalchemy.orm import Session
from mysqlapp.database import get_db
from fastapi import APIRouter,Depends, FastAPI, HTTPException
app_module=APIRouter(
    prefix='/modules',
    tags=['modules']
)

@app_module.put("/modules/{id_Module}", response_model=schemas.Module)
async def   update_module(id_Module: int, module: schemas.ModuleCreate, db: Session = Depends(get_db)):
    return crud.update_module(db=db, id_Module=id_Module, module=module)

@app_module.delete("/modules/{id_Module}", response_model=schemas.Module)
async def   delete_module(id_Module: int, db: Session = Depends(get_db)):
    return crud.delete_module(db=db, id_Module=id_Module)

@app_module.get("/modules/getby-id/{id_Module}", response_model=schemas.Module)
async def   read_module(id_Module: int, db: Session = Depends(get_db)):
    return crud.get_module(db,id_Module)

@app_module.get("/modules/getall",response_model=list[schemas.Module])
async def   read_module( skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    return crud.get_all_modules(db,skip=skip,limit=limit)

@app_module.post("/modules/create",response_model=schemas.Module)
async def   create_module(module:schemas.ModuleCreate,db:Session=Depends(get_db)):
    db_module=crud.get_module_by_name(db,nom_Module=module.nom_Module)
    if db_module:
        raise HTTPException(status_code=400,detail="Ce module existe déja")
    return crud.create_module(db=db,module=module)

@app_module.get("/modules/ofcours/{id_Cours}",response_model=list[schemas.Module])
async def   get_module_of_cours(id_Cours: int, db: Session = Depends(get_db)):
    db_mod=crud.get_cours(db,id_Cours)
    if db:
        return  crud.get_modules_for_cours(db,id_Cours)


