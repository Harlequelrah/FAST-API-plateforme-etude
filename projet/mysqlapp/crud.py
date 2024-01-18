from sqlalchemy.orm import Session,aliased
from sqlalchemy.sql import func
from . import models, schemas
from sqlalchemy import text
from typing import List,Tuple
from datetime import date
from enum import Enum
from fastapi import  HTTPException


def upid(db,max,id,id_column,table):
    if max:
           for i in range(id+1,max+2):
             db.execute(text(f"update {table} set {id_column}={i-1} where {id_column}={i}"))
             db.commit()

def create_etudiant(db: Session, etudiant: schemas.EtudiantCreate):


    fake_hashed_password = etudiant.mot_de_passe + "notreallyhashed"

    # Création d'une instance de l'étudiant avec le mot de passe hashé
    db_etudiant = models.Etudiant(
        nom_Etud=etudiant.nom_Etud,
        prenom_Etud=etudiant.prenom_Etud,
        email_Etud=etudiant.email_Etud,
        date_Naissance=etudiant.date_Naissance,
        universite_Provenance=etudiant.universite_Provenance,
        mot_de_passe=fake_hashed_password
    )

    # Ajout de l'étudiant à la session de base de données
    db.add(db_etudiant)
    max_id = db.query(func.max(models.Etudiant.id_Etud)).scalar()
    if max_id is not None:db.execute(text(f"ALTER TABLE etudiants AUTO_INCREMENT = {max_id + 1}"))
    # Validation des modifications dans la base de données
    db.commit()

    # Actualisation de l'objet étudiant pour refléter les éventuelles modifications dans la base de données
    db.refresh(db_etudiant)


    # Retourne l'objet étudiant créé
    return db_etudiant

#retourne un etudiant a partir de son identifiant
def get_etudiant(db:Session,id_Etud:int):
    db_etudiant= db.query(models.Etudiant).filter(models.Etudiant.id_Etud==id_Etud).first()
    if db_etudiant is None :
        raise HTTPException(status_code=404,detail ='Etudiant non trouvé')
    return db_etudiant

#retourne un etudiant a partir de son email
def get_etudiant_by_email(db:Session,email:str):
    db_etudiant= db.query(models.Etudiant).filter(models.Etudiant.email_Etud==email).first()
    # if db_etudiant is None :
    #     raise HTTPException(status_code=404,detail ='Etudiant non trouvé')
    return db_etudiant

#retourne une liste d etudiant
def get_etudiants(db:Session,skip:int=0,limit:int=None):
    return db.query(models.Etudiant).order_by(models.Etudiant.nom_Etud).offset(skip).limit(limit).all()

#retourne le nombre des etudiants
def get_count_etudiants(db:Session):
     return db.query(func.count(models.Etudiant.id_Etud)).scalar()

def delete_etudiant(db: Session, id_Etud: int):
    db_etudiant = get_etudiant(db, id_Etud)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail='Etudiant non trouvé')
    else :
        db.delete(db_etudiant)
        db.commit()
        max_etudiants=get_count_etudiants(db)
        upid(db,max_etudiants,id_Etud,"id_Etud","etudiants")
    return db_etudiant


def update_etudiant(db: Session, etudiant: schemas.EtudiantCreate, id_Etud: int):
    db_etudiant = get_etudiant(db, id_Etud)

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

#renvoie les etudiants qui font parti d un cours
def get_etudiants_in_cours(db:Session,id_Cours:int):
    cours=get_cours(db,id_Cours)
    if cours :return cours.etudiants

#renvoie le statut de l 'inscription d un etudiant à un cours
def get_etudiant_statut_inscription_cours(db:Session,id_Etud:int,id_Cours:int):
    inscription= db.query(models.Inscription).filter(models.Inscription.id_Etud == id_Etud and models.Inscription.id_Cours == id_Cours).first()
    if inscription:return inscription.status














def create_professeur(db: Session, professeur: schemas.ProfesseurCreate):
    fake_hashed_password = professeur.password_Prof + "notreallyhashed"
    db_professeur = models.Professeur(
        nom_Prof=professeur.nom_Prof,
        prenom_Prof=professeur.prenom_Prof,
        email_Prof=professeur.email_Prof,
        password_Prof=fake_hashed_password
    )
    db.add(db_professeur)
    max_id = db.query(func.max(models.Professeur.id_Prof)).scalar()
    if max_id is not None:db.execute(text(f"ALTER TABLE professeurs AUTO_INCREMENT = {max_id + 1}"))
    db.commit()
    db.refresh(db_professeur)
    return db_professeur

# Fonction pour récupérer un professeur par son identifiant
def get_professeur(db: Session, id_Prof: int):
    db_professeur =db.query(models.Professeur).filter(models.Professeur.id_Prof == id_Prof).first()
    if db_professeur is None :
        raise HTTPException(status_code=404,detail ='Professeur non trouvé')
    return db_professeur


# Fonction pour récupérer un professeur par son email
def get_professeur_by_email(db: Session, email: str):
    db_professeur =db.query(models.Professeur).filter(models.Professeur.email_Prof == email).first()
    # if db_professeur is None :
    #     raise HTTPException(status_code=404,detail ='Professeur non trouvé')
    return db_professeur

# Fonction pour récupérer une liste de professeurs
def get_professeurs(db: Session, skip: int = 0, limit: int = None):
    return db.query(models.Professeur).order_by(models.Professeur.nom_Prof).offset(skip).limit(limit).all()

# Fonction pour compter le nombre de professeurs
def get_count_professeurs(db: Session):
    return db.query(func.count(models.Professeur.id_Prof)).scalar()

# Fonction pour supprimer un professeur
def delete_professeur(db: Session, id_Prof: int):
    db_professeur = db.query(models.Professeur).filter(models.Professeur.id_Prof == id_Prof).first()
    if db_professeur is None:
        raise HTTPException(status_code=404, detail='Professeur non trouvé')
    else:
        db.delete(db_professeur)
        db.commit()
        max_professeurs=get_count_professeurs(db)
        upid(db,max_professeurs,id_Prof,"id_Prof","professeurs")
    return db_professeur

# Fonction pour mettre à jour un professeur
def update_professeur(db: Session, id_Prof: int, professeur: schemas.ProfesseurCreate):
    db_professeur = db.query(models.Professeur).filter(models.Professeur.id_Prof == id_Prof).first()

    if db_professeur is None:
        raise HTTPException(status_code=404, detail='Professeur non trouvé')

    # Mise à jour des champs du professeur
    if professeur.nom_Prof is not None:
        db_professeur.nom_Prof = professeur.nom_Prof
    if professeur.prenom_Prof is not None:
        db_professeur.prenom_Prof = professeur.prenom_Prof
    if professeur.email_Prof is not None:
        db_professeur.email_Prof = professeur.email_Prof
    if professeur.password_Prof is not None:
        db_professeur.password_Prof = professeur.password_Prof

    db.commit()
    db.refresh(db_professeur)
    return db_professeur










# Fonction pour récupérer les cours enseignés par un professeur
def get_cours_by_professeur(db: Session, id_Prof: int):
    professeur = get_professeur(db, id_Prof)
    if professeur:
        return professeur.cours
    return []



#renvoie un cours à partir de son identifiant
def get_cours(db:Session,id_Cours:int):
    return db.query(models.Cours).filter(models.Cours.id_Cours==id_Cours).first()
#retourne les cours d un etudiant
def get_cours_in_etudiant(db: Session, id_Etud: int):
    return (
        db.query(models.Cours)
        .join(models.Etudiant, models.Cours.etudiants)
        .filter(models.Etudiant.id_Etud == id_Etud)
        .order_by(models.Cours.nom_Cours)
        .distinct()
    )
#retourne les cours par modules d ' un etudiant
def get__cours_in_etudiant_per_modules(db: Session, id_Etud: int):
    return (
        db.query(models.Cours, models.Module)
        .join(models.Etudiant, models.Cours.etudiants)
        .join(models.Module, models.Cours.modules)
        .filter(models.Etudiant.id_Etud == id_Etud)
        .group_by(models.Module.nom_Module)
        .order_by(models.Cours.nom_Cours)
        .all()
    )

def get_all_cours(db:Session,skip:int=0,limit:int=None):
    return db.query(models.Cours).order_by(models.Cours.nom_Cours).offset(skip).limit(limit).all()


def delete_cours(db: Session, id_Cours: int):
    db_cours = db.query(models.Cours).filter(models.Cours.id_Cours == id_Cours).first()
    if db_cours is None:
        raise HTTPException(status_code=404, detail='cours non trouvé')
    else:
        db.delete(db_cours)
        db.commit()
        max_cours=db.query(func.count(models.Cours.id_Cours)).scalar()
        upid(db,max_cours,id_Cours,"id_Cours","cours")
    return db_cours

def create_cours(db: Session, cours: schemas.CoursCreate):
    # Création d'une instance de cours
    db_cours = models.Cours(
        nom_Cours=cours.nom_Cours,
        libelle_Cours=cours.libelle_Cours,
        contenue_text=cours.contenue_text,
        contenue_binary=cours.contenue_binary
    )
    db.add(db_cours)
    max_id = db.query(func.max(models.Cours.id_Cours)).scalar()
    if max_id is not None:db.execute(text(f"ALTER TABLE cours AUTO_INCREMENT = {max_id + 1}"))
    db.commit()
    db.refresh(db_cours)
    return db_cours






#renvoie les modules dont fait parti un cours
def get_modules_of_cours(db:Session,id_Cours:int):
    cours=get_cours(db,id_Cours)
    if cours :return cours.modules



def get_cours_statuts_inscription(db: Session, id_Cours: int):
    E = aliased(models.Etudiant)
    resultats = (
        db.query(E.id_Etud, E.nom_Etud, E.prenom_Etud, models.Inscription.Status, models.Cours.id_Cours, models.Cours.nom_Cours)
        .join(models.Inscription)
        .join(E, E.id_Etud)
        .join(models.Cours, models.Cours.id_Cours)
        .filter(models.Inscription.id_Cours == id_Cours)
        .all()
    )
    return resultats

def get_cours_statut_inscription(db: Session, id_Cours: int, statut: str):
    E = aliased(models.Etudiant)
    resultats = (
        db.query(E.id_Etud, E.nom_Etud, E.prenom_Etud, models.Inscription.Status, models.Cours.id_Cours, models.Cours.nom_Cours)
        .join(models.Inscription)
        .join(E, E.id_Etud)
        .join(models.Cours, models.Cours.id_Cours)
        .filter(models.Inscription.id_Cours == id_Cours, models.Inscription.Status.in_(statut))
        .all()
    )
    return resultats

def update_inscription(db: Session, id_Etud: int, id_Cours: int, inscription_update: schemas.InscriptionCreate):
    db_inscription = db.query(models.Inscription).filter(
        models.Inscription.id_Etud == id_Etud,
        models.Inscription.id_Cours == id_Cours
    ).first()

    if db_inscription is None:
        return None

    # Mise à jour des champs modifiables
    db_inscription.id_Session = inscription_update.id_Session
    db_inscription.date_Inscription = inscription_update.date_Inscription
    db_inscription.Status = inscription_update.status
    db.commit()
    db.refresh(db_inscription)
    return db_inscription

def delete_inscription(db: Session, id_Etud: int, id_Cours: int):
    db_inscription = db.query(models.Inscription).filter(
        models.Inscription.id_Etud == id_Etud,
        models.Inscription.id_Cours == id_Cours
    ).first()

    if db_inscription:
        db.delete(db_inscription)
        db.commit()
        return db_inscription

    return None

def get_inscription_from_date(db: Session, date: date):
    return db.query(models.Inscription).filter(models.Inscription.date_Inscription == date).all()



def get_all_modules(db:Session,skip:int=0,limit:int=None):
     return db.query(models.Module).order_by(models.Module.nom_Module).offset(skip).limit(limit).all()



def get_module(db:Session,id_Module:int):
     return db.query(models.Module).filter(models.Module.id_Module==id_Module).first()

def get_module_by_name(db:Session,nom_Module:int):
     return db.query(models.Module).filter(models.Module.nom_Module==nom_Module).first()

def delete_module(db: Session, id_Module: int):
    db_module = db.query(models.Module).filter(models.Module.id_Module == id_Module).first()
    if db_module is None:
        raise HTTPException(status_code=404, detail='Module non trouvé')
    else:
        db.delete(db_module)
        db.commit()
        max_modules=db.query(func.count(models.Module.id_Module)).scalar()
        upid(db,max_modules,id_Module,"id_Module","modules")
    return db_module

def update_module(db: Session, id_Module: int, module: schemas.ModuleCreate):
    db_module = db.query(models.Module).filter(models.Module.id_Module == id_Module).first()

    if db_module is None:
        raise HTTPException(status_code=404, detail='Professeur non trouvé')

    # Mise à jour des champs du professeur
    if module.nom_Module is not None:
        db_module.nom_Module = module.nom_Module
    if module.libelle_Module is not None:
        db_module.libelle_Module = module.libelle_Module


    db.commit()
    db.refresh(db_module)
    return db_module



def create_module(db: Session, module: schemas.ModuleCreate):
    db_module = models.Module(
        nom_Module=module.nom_Module,
        libelle_Module=module.libelle_Module
    )
    db.add(db_module)
    max_id = db.query(func.max(models.Module.id_Module)).scalar()
    if max_id is not None:db.execute(text(f"ALTER TABLE modules AUTO_INCREMENT = {max_id + 1}"))
    db.commit()
    db.refresh(db_module)
    return db_module

def get_modules_for_cours(db: Session, id_Cours: int):
    # Requête pour récupérer les modules associés à un cours spécifique
    modules = db.query(models.Module).join(models.Contenir).filter(models.Contenir.id_Cours == id_Cours).all()
    return modules



def create_inscription(db: Session, inscription: schemas.InscriptionCreate):
    db_inscription = models.Inscription(
        id_Session=inscription.id_Session,
        date_Inscription=inscription.date_Inscription,
        status=inscription.status,
        id_Etud=inscription.id_Etud,
        id_Cours=inscription.id_Cours
    )
    db.add(db_inscription)
    db.commit()
    db.refresh(db_inscription)
    return db_inscription





def create_enseigner(db: Session, enseigner: schemas.EnseignerCreate):
    db_enseigner = models.Enseigner(
        session_Debut=enseigner.session_Debut,
        session_Fin=enseigner.session_Fin,
        volume_Horaire=enseigner.volume_Horaire,
        id_Prof=enseigner.id_Prof,
        id_Cours=enseigner.id_Cours
    )
    db.add(db_enseigner)
    db.commit()
    db.refresh(db_enseigner)
    return db_enseigner

def delete_enseigner(db: Session, id_Prof: int, id_Cours: int):
    db_enseigner = db.query(models.Enseigner).filter(
        models.Enseigner.id_Prof == id_Prof, models.Enseigner.id_Cours == id_Cours
    ).first()

    if db_enseigner:
        db.delete(db_enseigner)
        db.commit()
        return db_enseigner
    else:
        return None
def get_enseigner_by_ids(db: Session, id_Prof: int, id_Cours: int):
    return db.query(models.Contenir).filter(
        models.Enseigner.id_Cours == id_Cours,
        models.Enseigner.id_Prof == id_Prof
    ).first()







def get_contenir_by_ids(db: Session, id_cours: int, id_module: int):
    return db.query(models.Contenir).filter(
        models.Contenir.id_Cours == id_cours,
        models.Contenir.id_Module == id_module
    ).first()

