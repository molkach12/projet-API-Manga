from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Token secret pour sécuriser l'accès
SECRET_TOKEN = "123abc"

# Exemple statique de personnages (GET)
personnages = [
    {"id": 1, "nom": "Harry Potter", "univers": "Harry Potter"},
    {"id": 2, "nom": "Luke Skywalker", "univers": "Star Wars"},
    {"id": 3, "nom": "Tony Stark", "univers": "Marvel"},
    {"id": 4, "nom": "Geralt de Riv", "univers": "The Witcher"}
]

# Middleware CORS pour autoriser les appels depuis d'autres apps (ex : front-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === GET /personnages ===
@app.get("/personnages")
def get_personnages(token: str = Header(...)):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token invalide")
    return personnages

# === Modèle Pydantic pour POST /scores ===
class Score(BaseModel):
    nom: str
    ville: str
    revenu: float
    avis: str

# === POST /scores ===
@app.post("/scores")
def create_score(score: Score, token: str = Header(...)):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token invalide")

    print(f"✅ Score reçu : {score}")
    return {
        "message": "Score bien enregistré",
        "data": score
    }

from pydantic import BaseModel

# === Modèle Pydantic pour traitement ===
class DonneeTraitee(BaseModel):
    nom: str
    score: int

# === Endpoint POST /traitement ===
@app.post("/traitement")
def traitement(p: DonneeTraitee):
    if p.score >= 90:
        niveau = "expert"
    elif p.score >= 70:
        niveau = "confirmé"
    elif p.score >= 50:
        niveau = "intermédiaire"
    else:
        niveau = "débutant"

    return {
        "nom": p.nom,
        "score": p.score,
        "niveau": niveau
    }
