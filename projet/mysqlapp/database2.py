from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
username=""
password=""
# URL de la base de données MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://"+username+":@"+password+"@localhost/plateforme-etude"

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Utile pour vérifier la connexion à la base de données
)

# Session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base déclarative SQLAlchemy
Base = declarative_base()
