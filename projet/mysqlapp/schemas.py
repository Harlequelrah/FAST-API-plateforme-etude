from typing import List, Optional,Tuple
from enum import Enum
from datetime import date,time
from pydantic import BaseModel,validator,Field


class EtudiantBase(BaseModel):
    nom_Etud:str=Field(examples=['AKIRA'])
    prenom_Etud: str=Field(examples=['john smith'])
    email_Etud: str
    date_Naissance: date
    universite_Provenance: str

class EtudiantUpdate(BaseModel):
    nom_Etud:Optional[str]=Field(examples=['AKIRA'])
    prenom_Etud: Optional[str]=Field(examples=['john smith'])
    email_Etud: Optional[str]
    date_Naissance: Optional[date]=None
    universite_Provenance: Optional[str]=None

class EtudiantCreate(EtudiantBase):
     mot_de_passe: str

class Etudiant(EtudiantBase):
    id_Etud: int
    cours: List["Cours"] = []

    class Config:
        from_orm = True


class CoursBase(BaseModel):
    nom_Cours: str=None
    libelle_Cours: str=None
    contenue_text: str=None  # Pour le texte
    contenue_binary: bytes=None  # Pour les données binaires


class CoursUpdate(BaseModel):
    nom_Cours: Optional[str]=None
    libelle_Cours: Optional[str]=None
    contenue_text: Optional[str]=None  # Pour le texte
    contenue_binary: Optional[bytes]=None  # Pour les données binaires

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
    en_attente=("EN_ATTENTE","en_attente")
    validee=("Validee","validee")
    annulee=("Annulee","annulee")

class InscriptionBase(BaseModel):

    id_Session: int=None
    date_Inscription: date=None
    status:Optional[InscriptionStatus]=Field(examples=['en_cours'])

class InscriptionUpdate(BaseModel):

    id_Session:Optional [int]=None
    date_Inscription:Optional [date]=None
    status:Optional[InscriptionStatus]=Field(examples=['en_cours'])




class InscriptionCreate(InscriptionBase):
    pass


class Inscription(InscriptionBase):
    id_Etud: int
    id_Cours: int

    class Config:
        from_orm = True

class ProfesseurBase(BaseModel):
    nom_Prof: str=None
    prenom_Prof: str=None
    email_Prof: str=None

class ProfesseurUpdate(BaseModel):
    nom_Prof: Optional[str]=None
    prenom_Prof: Optional[str]=None
    email_Prof: Optional[str]=None

class ProfesseurCreate(ProfesseurBase):
    password_Prof: str

class Professeur(ProfesseurBase):
    id_Prof: int
    cours: List[Cours] = []

    class Config:
        from_orm = True

class EnseignerBase(BaseModel):
    session_Debut: date=None
    session_Fin: date=None
    volume_Horaire: time=None

class EnseignerUpdate(BaseModel):
    session_Debut: Optional[date]=None
    session_Fin: Optional[date]=None
    volume_Horaire: Optional[time]=None

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
    nom_Module: str=None
    libelle_Module: str=None

class ModuleUpdate(BaseModel):
    nom_Module: Optional[str]=None
    libelle_Module: Optional[str]=None

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
