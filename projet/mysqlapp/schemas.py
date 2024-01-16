from typing import List, Optional,Tuple
from enum import Enum
from datetime import date,time
from pydantic import BaseModel,validator,Field


class EtudiantBase(BaseModel):
    nom_Etud: str=Field(examples=['AKIRA'])
    prenom_Etud: str=Field(examples=['john smith'])
    email_Etud: str
    date_Naissance: date
    universite_Provenance: str

class EtudiantCreate(EtudiantBase):
     mot_de_passe: str

class Etudiant(EtudiantBase):
    id_Etud: int
    cours: List["Cours"] = []

    class Config:
        from_orm = True


class CoursBase(BaseModel):
    nom_Cours: str
    libelle_Cours: str
    contenue_text: Optional[str]  # Pour le texte
    contenue_binary: Optional[bytes]  # Pour les données binaires

class CoursCreate(CoursBase):
    pass

class Cours(CoursBase):
    id_Cours: int
    etudiants: List[Etudiant] = []
    professeurs: List["Professeur"] = []
    modules: List["Module"] = []

    class Config:
        from_orm = True

class InscriptionStatus(Enum):
    en_cours=("EN_COURS","en_cours")
    en_attente=("EN_ATTENTE","en_cours")
    validee=("Validee","validee")
    annulee=("Annulee","annulee")
class InscriptionBase(BaseModel):

    id_Session: int
    date_Inscription: date
    status:InscriptionStatus



class InscriptionCreate(InscriptionBase):
    pass


class Inscription(InscriptionBase):
    id_Etud: int
    id_Cours: int

    class Config:
        from_orm = True

class ProfesseurBase(BaseModel):
    nom_Prof: str
    prenom_Prof: str
    email_Prof: str

class ProfesseurCreate(ProfesseurBase):
    password_Prof: str

class Professeur(ProfesseurBase):
    id_Prof: int
    cours: List[Cours] = []

    class Config:
        from_orm = True

class EnseignerBase(BaseModel):
    session_Debut: date
    session_Fin: date
    volume_Horaire: time

    @validator("session_Debut", pre=True, always=True)
    def validate_session_Debut(cls, value):
        if value <= date.today():
            raise ValueError("La date de début de session doit être ultérieure à la date actuelle")
        return value

    @validator("session_Debut", "session_Fin", pre=True, always=True)
    def validate_sessions(cls, values):
        session_Debut, session_Fin = values.get("session_Debut"), values.get("session_Fin")
        if session_Debut and session_Fin and session_Debut > session_Fin:
            raise ValueError("La date de début de session doit être antérieure à la date de fin")
        return values

class EnseignerCreate(EnseignerBase):
    pass

class Enseigner(EnseignerBase):
    id_Prof: int
    id_Cours: int

    class Config:
        from_orm = True

class ModuleBase(BaseModel):
    nom_Module: str
    libelle_Module: str

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id_Module: int
    cours: List[Cours] = []

    class Config:
        from_orm = True

class ContenirBase(BaseModel):
    pass

class ContenirCreate(ContenirBase):
    pass

class Contenir(ContenirBase):
    id_Cours: int
    id_Module: int

    class Config:
        from_orm = True
