from sqlalchemy import Boolean,TEXT, LargeBinary ,Column, Time,ForeignKey, Integer, String,Date, Text,Sequence
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from .database import Base


class Etudiant(Base):
    __tablename__='etudiants'
    id_Etud=Column(Integer,primary_key=True,index=True)
    nom_Etud=Column(String(30),nullable=False)
    prenom_Etud=Column(String(30),nullable=False)
    email_Etud=Column(String(50),unique=True,nullable=False)
    mot_de_passe=Column(String(100),nullable=False)
    date_Naissance=Column(Date,nullable=False)
    universite_Provenance=Column(String(50),nullable=False)
    cours=relationship("Cours",back_populates="etudiants",secondary="inscriptions")

class Cours(Base):
   __tablename__='cours'
   id_Cours=Column(Integer,primary_key=True,index=True)
   nom_Cours=Column(String(30),nullable=False,index=True)
   libelle_Cours=Column(String(50),nullable=False)
   contenue_text = Column(Text, nullable=True)  # Pour le texte
   contenue_binary = Column(LargeBinary, nullable=True)  # Pour les données binaires

   etudiants=relationship("Etudiant",back_populates="cours",secondary="inscriptions")
   professeurs=relationship("Professeur",back_populates="cours",secondary="enseigner")
   modules=relationship("Module",back_populates="cours",secondary="contenir")



class Inscription(Base):
    INSCRIPTION_STATUS=(("EN_COURS","en_cours"),("EN_ATTENTE","en_attente"),("Validee","validee"),("Annulee","annulee"))
    __tablename__ = 'inscriptions'
    id_Etud = Column(Integer,ForeignKey("etudiants.id_Etud"),primary_key=True,index=True)
    id_Cours = Column(Integer,ForeignKey("cours.id_Cours"),primary_key=True,index=True)
    id_Session = Column(Integer,index=True,nullable=False)
    date_Inscription=Column(Date,nullable=False)
    Status=Column(ChoiceType(INSCRIPTION_STATUS),default="EN_COURS")


class Professeur(Base):
    __tablename__='professeurs'
    id_Prof=Column(Integer,primary_key=True,index=True)
    nom_Prof=Column(String(30),nullable=False)
    prenom_Prof=Column(String(30),nullable=False)
    email_Prof=Column(String(50),unique=True,nullable=False)
    password_Prof=Column(String(100),nullable=False)
    cours=relationship("Cours",back_populates="professeurs",secondary="enseigner")

class Enseigner(Base):
    __tablename__='enseigner'
    id_Prof = Column(Integer,ForeignKey("professeurs.id_Prof"),primary_key=True,index=True)
    id_Cours = Column(Integer,ForeignKey("cours.id_Cours"),primary_key=True,index=True)
    session_Debut=Column(Date,nullable=False)
    session_Fin=Column(Date,nullable=False)
    volume_Horaire=Column(Time,nullable=False)

class Module(Base):
 __tablename__="modules"
 id_Module=Column(Integer,primary_key=True,index=True)
 nom_Module=Column(String(30),nullable=False,index=True)
 libelle_Module=Column(String(50),nullable=False)
 cours=relationship("Cours",back_populates="modules",secondary="contenir")

class Contenir(Base):
    __tablename__="contenir"
    id_Cours = Column(Integer,ForeignKey("cours.id_Cours"),primary_key=True,index=True)
    id_Module = Column(Integer,ForeignKey("modules.id_Module"),primary_key=True,index=True)


