from typing import List, Optional,Tuple
from enum import Enum
from datetime import date,time
from pydantic import BaseModel,validator,Field

class Universite(str, Enum):
    IAI_TOGO = 'IAI-TOGO'
    ESGIS = 'ESGIS'
    UCAO = 'UCAO'
    UNIVERSITE_DE_LOME = 'UNIVERSITE de Lomé'
    COLLEGE_DE_PARIS_SUPERIEUR = 'College de Paris Superieur'


class EtudiantBase(BaseModel):
    nom_Etud:str=Field(examples=['AKIRA'])
    prenom_Etud: str=Field(examples=['john smith'])
    email_Etud: str=Field(examples=['underworld@gmail.com'])
    date_Naissance: date
    universite_Provenance: Universite

class EtudiantUpdate(BaseModel):
    nom_Etud:Optional[str]=Field(examples=['AKIRA'])
    prenom_Etud: Optional[str]=Field(examples=['john smith'])
    email_Etud: Optional[str]
    date_Naissance: Optional[date]=None
    universite_Provenance: Optional[Universite]=None

class EtudiantCreate(EtudiantBase):
    mot_de_passe: str

class Etudiant(EtudiantBase):
    id_Etud: int
    cours: List[int] = []


    class Config:
        from_orm = True

from typing import List, Optional
from pydantic import BaseModel, Field

class CoursBase(BaseModel):
    nom_Cours: str = Field(..., max_length=30)
    libelle_Cours: str = Field(..., max_length=50)
    contenue_text: Optional[str] = None
    urls_contenue: Optional[str] = None

class CoursUpdate(BaseModel):
    nom_Cours: Optional[str] = None
    libelle_Cours: Optional[str] = None
    contenue_text: Optional[str] = None
    urls_contenue: Optional[str] = None

class CoursCreate(CoursBase):
    pass

class Cours(CoursBase):
    id_Cours: int
    etudiants: List[int] = []
    professeurs: List[int] = []
    modules: List[int] = []

    class Config:
        from_orm = True

class INSCRIPTION_STATUS(str, Enum):
    EN_COURS = "EN_COURS"
    EN_ATTENTE = "EN_ATTENTE"
    VALIDE = "Validee"
    ANNULEE = "Annulee"


class InscriptionBase(BaseModel):
    id_Etud: int
    id_Cours: int
    id_Session: int = None
    date_Inscription: date = None
    Status: INSCRIPTION_STATUS = Field(..., description="Status de l'inscription (EN_COURS, EN_ATTENTE, VALIDE, ANNULEE)")


class InscriptionUpdate(BaseModel):
    id_Session: Optional[int] = None
    date_Inscription: Optional[date] = None
    Status: Optional[INSCRIPTION_STATUS] = Field(None, description="Status de l'inscription (EN_COURS, EN_ATTENTE, VALIDE, ANNULEE)")


class InscriptionCreate(InscriptionBase):
    pass


class Inscription(InscriptionBase):
    pass

    class Config:
        from_orm = True

class ProfesseurBase(BaseModel):
    nom_Prof: str=None
    prenom_Prof: str=None
    email_Prof: str=None


# class ProfesseurResponse(BaseModel):
#     nom_Prof: str=None
#     prenom_Prof: str=None
#     email_Prof: str=None



class ProfesseurUpdate(BaseModel):
    nom_Prof: Optional[str]=None
    prenom_Prof: Optional[str]=None
    email_Prof: Optional[str]=None

class ProfesseurCreate(ProfesseurBase):
    password_Prof: str

class Professeur(ProfesseurBase):
    id_Prof: int
    cours: List[int] = []

    class Config:
        from_orm = True


class EnseignerBase(BaseModel):
    session_Debut: date=None
    session_Fin: date=None
    volume_Horaire: int=None
    id_Prof: int=None
    id_Cours: int=None

class EnseignerUpdate(BaseModel):
    id_Prof: Optional[int]
    id_Cours: Optional[int]
    session_Debut: Optional[date]=None
    session_Fin: Optional[date]=None
    volume_Horaire: Optional[int]=None

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
    pass


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
    cours: List[int] = []

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
