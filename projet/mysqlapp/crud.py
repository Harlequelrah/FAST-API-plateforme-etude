from sqlalchemy.orm import Session,aliased
from sqlalchemy.sql import func
from . import models, schemas
from typing import List,Tuple
from datetime import date

#retourne un etudiant a partir de son identifiant
def get_etudiant(db:Session,id_Etud:int):
    return db.query(models.Etudiant).filter(models.Etudiant.id_Etud==id_Etud).first()

#retourne un etudiant a partir de son email
def get_etudiant_by_email(db:Session,email:str):
    return db.query(models.Etudiant).filter(models.Etudiant.email==email).first()

#retourne une liste d etudiant
def get_etudiants(db:Session,skip:int=0,limit:int=None):
    return db.query(models.Etudiant).offset(skip).limit(limit).order_by(models.Etudiant.nom_Etud).all()

#retourne le nombre des etudiants
def get_count_etudiants(db:Session):
     return db.query(func.count(models.Etudiant.id_Etud)).scalar()


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

#retourne les cours d un etudiant
def get_cours_in_etudiant(db: Session, id_Etud: int):
    return (
        db.query(models.Cours)
        .join(models.Etudiant, models.Cours.etudiants)
        .filter(models.Etudiant.id_Etud == id_Etud)
        .order_by(models.Cours.nom_Cours)
        .distinct()
    )


#renvoie un cours à partir de son identifiant
def get_cours(db:Session,id_Cours:int):
    return db.query(models.Cours).filter(models.Cours.id_Cours==id_Cours).first()

#renvoie les etudiants qui font parti d un cours
def get_etudiants_in_cours(db:Session,id_Cours:int):
    cours=get_cours(db,id_Cours)
    if cours :return cours.etudiants

#renvoie les professeurs qui enseigne un cours
def get_professeur_in_cours(db:Session,id_Cours:int):
    cours=get_cours(db,id_Cours)
    if cours :return cours.professeurs


#renvoie les modules dont fait parti un cours
def get_modules_of_cours(db:Session,id_Cours:int):
    cours=get_cours(db,id_Cours)
    if cours :return cours.modules

#renvoie le statut de l 'inscription d un etudiant à un cours
def get_etudiant_statut_inscription_cours(db:Session,id_Etud:int,id_Cours:int):
    inscription= db.query(models.Inscription).filter(models.Inscription.id_Etud == id_Etud and models.Inscription.id_Cours == id_Cours).first()
    if inscription:return inscription.status

#renvoie des informations sur les etudiant et leurs  statuts d inscription à un cours
def get_cours_statuts_inscription(db:Session,id_Cours:int):
    E=aliased(models.Etudiant)
    resultats=(
        db.query(E.id_Etud,E.nom_Etud,E.prenom_Etud,models.Inscription.Status,models.Cours.id_Cours,models.Cours.nom_Cours)
        .join(models.Inscription)
        .join(E,E.id_Etud)
        .join(models.Cours,models.Cours.id_Cours)
        .filter(models.Inscription.id_Cours==id_Cours)
        .all()
    )
    return resultats

#renvoie des informations sur les etudiant et leurs  statuts d inscription à un cours en specifiant un statut
def get_cours_statut_inscription(db:Session,id_Cours:int,statut:Tuple(str,str)):
    E=aliased(models.Etudiant)
    resultats=(
        db.query(E.id_Etud,E.nom_Etud,E.prenom_Etud,models.Inscription.Status,models.Cours.id_Cours,models.Cours.nom_Cours)
        .join(models.Inscription)
        .join(E,E.id_Etud)
        .join(models.Cours,models.Cours.id_Cours)
        .filter(models.Inscription.id_Cours==id_Cours and models.Inscription.Status in statut)
        .all()
    )
    return resultats


#retourne toutes les inscriptions qui ont eu lieu a une date precise
def get_inscription_from_date(db:Session,date:date):
    return db.query(models.Inscription).filter(models.Inscription.date_Inscription == date).all()



# def get_professeur(db:Session,id_Prof:int):
#     return db.query(models.Professeur).filter(models.Professeur.id_Prof==id_Prof).first()

# def get_module(db:Session,id_Module:int):
#     return db.query(models.Module).filter(models.Module.id_Module==id_Module).first()

# def get_cours(db:Session,id_Cours:int):
#     return db.query(models.Cours).filter(models.Cours.id_Cours==id_Cours).first()


