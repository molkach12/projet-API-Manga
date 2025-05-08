from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

app = FastAPI()

# === Configuration de CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Configuration de la base de données SQLite ===
DATABASE_URL = "sqlite:///./personnages.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# === Modèle SQLAlchemy pour la table "personnages" ===
class PersonnageDB(Base):
    __tablename__ = "personnages"
    id = Column(String, primary_key=True, index=True)
    nom = Column(String, index=True)
    score = Column(Integer)
    niveau = Column(String)

# Créer la table si elle n'existe pas
Base.metadata.create_all(bind=engine)

# === Modèle Pydantic pour les entrées ===
class PersonnageWebhook(BaseModel):
    nom: str
    score: int

# === Configuration JWT et utilisateur fictif ===
SECRET_KEY = "une_clé_ultra_secrète_à_modifier"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

fake_user = {
    "username": "mikou",
    "hashed_password": "$2b$12$8RCkZ5khXCWytkJVpsJikuvn3ILyE3t07SZGzZ//WkwDD34.qYBuu"  # = mikou
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# === Fonctions de sécurité ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != fake_user["username"]:
            raise HTTPException(status_code=401, detail="Utilisateur invalide")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# === Dépendance pour accéder à la base de données ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Route POST /login : connexion et génération de token ===
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or not verify_password(form_data.password, fake_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    access_token = create_access_token(data={"sub": fake_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# === Route POST /webhook/personnage : enregistrement en base ===
@app.post("/webhook/personnage")
def recevoir_personnage(personnage: PersonnageWebhook, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    # Déterminer le niveau en fonction du score
    if personnage.score >= 90:
        niveau = "expert"
    elif personnage.score >= 70:
        niveau = "confirmé"
    elif personnage.score >= 50:
        niveau = "intermédiaire"
    else:
        niveau = "débutant"

    identifiant = str(uuid.uuid4())

    nouveau = PersonnageDB(id=identifiant, nom=personnage.nom, score=personnage.score, niveau=niveau)
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)

    print(f"📝 Enregistré : {nouveau.nom} (ID: {nouveau.id})")

    return {
        "id": nouveau.id,
        "nom": nouveau.nom,
        "score": nouveau.score,
        "niveau": nouveau.niveau
    }

# === Route GET /personnage/{id} : récupérer un personnage ===
@app.get("/personnage/{personnage_id}")
def lire_personnage(personnage_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    personnage = db.query(PersonnageDB).filter(PersonnageDB.id == personnage_id).first()
    if not personnage:
        raise HTTPException(status_code=404, detail="Personnage introuvable")

    return {
        "id": personnage.id,
        "nom": personnage.nom,
        "score": personnage.score,
        "niveau": personnage.niveau
    }

# === Route GET /dashboard : affichage HTML de tous les personnages ===
@app.get("/dashboard", response_class=HTMLResponse)
def afficher_dashboard(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    personnages = db.query(PersonnageDB).all()

    html = """
    <html>
        <head>
            <title>Dashboard Personnages</title>
            <style>
                body { font-family: Arial; margin: 40px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 8px 12px; border: 1px solid #ccc; }
                th { background-color: #f2f2f2; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
            <h1>📊 Dashboard des Personnages</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Score</th>
                    <th>Niveau</th>
                </tr>
    """

    for p in personnages:
        html += f"""
        <tr>
            <td>{p.id}</td>
            <td>{p.nom}</td>
            <td>{p.score}</td>
            <td>{p.niveau}</td>
        </tr>
        """

    html += """
            </table>
        </body>
    </html>
    """

    return HTMLResponse(content=html)
