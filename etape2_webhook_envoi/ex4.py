from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import requests

app = FastAPI()

# === Fichier de log et de notification ===
LOG_FILE = "webhook_log.json"
NOTIF_FILE = "notifications.txt"

# === Modèle pour le personnage reçu ===
class Personnage(BaseModel):
    nom: str
    score: int

# === Webhook principal : recevoir un personnage ===
@app.post("/webhook/personnage")
async def recevoir_personnage(p: Personnage):
    print(f"🎯 Personnage reçu : {p.nom}, score : {p.score}")

    # Étape 1 : calcul du niveau
    if p.score >= 90:
        niveau = "expert"
    elif p.score >= 70:
        niveau = "confirmé"
    elif p.score >= 50:
        niveau = "intermédiaire"
    else:
        niveau = "débutant"

    data = {
        "nom": p.nom,
        "score": p.score,
        "niveau": niveau
    }

    # Étape 2 : enregistrement dans webhook_log.json
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    historique = json.load(f)
                except json.JSONDecodeError:
                    historique = []
        else:
            historique = []

        historique.append(data)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(historique, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement : {e}")

    # Étape 3 : notifier un abonné (console + fichier + appel local)
    print("🔔 Notification : Personnage ajouté avec succès !")

    # Écriture dans un fichier de notification
    with open(NOTIF_FILE, "a", encoding="utf-8") as notif:
        notif.write(f"📝 {p.nom} ajouté avec le niveau {niveau}\n")

    # Appel d’une route locale pour simuler un abonné actif
    try:
        requests.get("http://localhost:8000/notifier")
    except:
        print("⚠️ Route /notifier non disponible (simulation)")

    return {
        "message": "Personnage reçu et enregistré avec succès",
        "niveau": niveau
    }

# === Route abonné simulé ===
@app.get("/notifier")
def notifier():
    print("📢 [NOTIFIER] Un personnage vient d’être ajouté !")
    return {"status": "notification envoyée"}
