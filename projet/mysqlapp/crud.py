from sqlalchemy.orm import Session,aliased
from sqlalchemy.sql import func
from . import models, schemas
from typing import List,Tuple
from datetime import date
from enum import Enum

#retourne un etudiant a partir de son identifiant
def get_etudiant(db:Session,id_Etud:int):
    return db.query(models.Etudiant).filter(models.Etudiant.id_Etud==id_Etud).first()

#retourne un etudiant a partir de son email
def get_etudiant_by_email(db:Session,email:str):
    return db.query(models.Etudiant).filter(models.Etudiant.email_Etud==email).first()

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
def get_cours_statut_inscription(db:Session,id_Cours:int,statut:str):
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



def get_professeur(db:Session,id_Prof:int):
    return db.query(models.Professeur).filter(models.Professeur.id_Prof==id_Prof).first()


def get_module(db:Session,id_Module:int):
     return db.query(models.Module).filter(models.Module.id_Module==id_Module).first()


def get_cours(db:Session,id_Cours:int):
     return db.query(models.Cours).filter(models.Cours.id_Cours==id_Cours).first()


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

    # Validation des modifications dans la base de données
    db.commit()

    # Actualisation de l'objet étudiant pour refléter les éventuelles modifications dans la base de données
    db.refresh(db_etudiant)

    # Retourne l'objet étudiant créé
    return db_etudiant

def create_cours(db: Session, cours: schemas.CoursCreate):
    # Création d'une instance de cours
    db_cours = models.Cours(
        nom_Cours=cours.nom_Cours,
        libelle_Cours=cours.libelle_Cours,
        contenue=cours.contenue
    )


    db.add(db_cours)


    db.commit()


    db.refresh(db_cours)


    return db_cours


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


def create_professeur(db: Session, professeur: schemas.ProfesseurCreate):
    db_professeur = models.Professeur(
        nom_Prof=professeur.nom_Prof,
        prenom_Prof=professeur.prenom_Prof,
        email_Prof=professeur.email_Prof
    )
    db.add(db_professeur)
    db.commit()
    db.refresh(db_professeur)
    return db_professeur


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


def create_module(db: Session, module: schemas.ModuleCreate):
    db_module = models.Module(
        nom_Module=module.nom_Module,
        libelle_Module=module.libelle_Module
    )
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


def create_contenir(db: Session, contenir: schemas.ContenirCreate):
    db_contenir = models.Contenir(
        id_Cours=contenir.id_Cours,
        id_Module=contenir.id_Module
    )
    db.add(db_contenir)
    db.commit()
    db.refresh(db_contenir)
    return db_contenir
