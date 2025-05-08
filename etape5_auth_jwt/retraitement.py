import json
import requests

FICHIER = "webhook_log.json"  # Le fichier contenant les personnages
API_TRAITEMENT = "http://localhost:8000/traitement"  # L'endpoint FastAPI

# Lire les personnages depuis le fichier JSON
try:
    with open(FICHIER, "r", encoding="utf-8") as f:
        personnages = json.load(f)
except Exception as e:
    print(f"❌ Erreur de lecture du fichier : {e}")
    personnages = []
    # Supprimer les doublons de noms
uniques = {p["nom"]: p for p in personnages}
personnages = list(uniques.values())


print(f"\n🔄 Traitement de {len(personnages)} personnage(s)...\n")

# Appeler /traitement pour chaque personnage
for p in personnages:
    try:
        payload = {
            "nom": p["nom"],
            "score": p["score"]
        }
        response = requests.post(API_TRAITEMENT, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['nom']} (score : {data['score']}) → niveau : {data['niveau']}")

        else:
            print(f"❌ {p['nom']} : erreur {response.status_code}")

    except Exception as e:
        print(f"❌ Exception lors du traitement de {p.get('nom', 'inconnu')} : {e}")
