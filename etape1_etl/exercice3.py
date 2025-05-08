import requests
import json
import time

# === ÉTAPE 1 : EXTRACTION DES DONNÉES ===
def extract(base_url, max_retries=3, timeout=5):
    """
    Extrait les données paginées depuis l'API avec gestion des erreurs et retry.
    """
    toutes_donnees = []
    page = 0

    while True:
        print(f"📥 Extraction - Récupération de la page {page}...")

        for attempt in range(max_retries):
            try:
                response = requests.get(base_url + str(page), timeout=timeout)
                if response.status_code == 200:
                    break
                else:
                    print(f"❌ Erreur HTTP : {response.status_code}")
                    return toutes_donnees
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Tentative {attempt + 1}/{max_retries} échouée : {e}")
                time.sleep(1)

        else:
            print("❌ Échec après plusieurs tentatives.")
            break

        data = response.json()

        if not data['organizations']:
            print("✅ Plus de résultats à extraire.")
            break

        toutes_donnees.extend(data['organizations'])
        page += 1
        time.sleep(0.5)

    return toutes_donnees

# === ÉTAPE 2 : TRANSFORMATION + DEBUG ===
def transform(donnees_brutes):
    """
    Filtre les données avec city défini et affiche un aperçu des revenus.
    """
    print("🔄 Transformation - Filtrage par 'city' défini uniquement...")

    donnees_filtrees = []
    revenus = []

    for org in donnees_brutes:
        city = org.get('city')
        income = org.get('income_amount')

        # Debugging : affichage pour inspection
        print(f"city: {city}, income_amount: {income}")

        if city:
            donnees_filtrees.append(org)

            # Collecte des revenus même s'ils sont 0 ou non définis
            if isinstance(income, (int, float)):
                revenus.append(income)

    moyenne_revenu = sum(revenus) / len(revenus) if revenus else 0

    print(f"✅ Organisations conservées : {len(donnees_filtrees)}")
    print(f"📊 Revenu moyen (si défini) : {round(moyenne_revenu, 2)} $")

    return donnees_filtrees, moyenne_revenu

# === ÉTAPE 3 : CHARGEMENT ===
def load(donnees, chemin_fichier):
    """
    Sauvegarde les données transformées dans un fichier JSON.
    """
    print(f"💾 Chargement - Sauvegarde dans le fichier {chemin_fichier}...")
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
    print("✅ Données sauvegardées avec succès.")

# === PIPELINE PRINCIPALE ===
def main():
    base_url = "https://projects.propublica.org/nonprofits/api/v2/search.json?q=chat&page="

    # Étape 1 : Extraire
    donnees_brutes = extract(base_url)

    # 🧪 Aperçu brut : voir ce qu'on récupère
    print("\n🧪 Exemple brut (1er élément) :")
    if donnees_brutes:
        print(json.dumps(donnees_brutes[0], indent=4))
    else:
        print("Aucune donnée brute reçue.")

    # Étape 2 : Transformer
    donnees_filtrees, moyenne_revenu = transform(donnees_brutes)

    # Étape 3 : Charger
    load(donnees_filtrees, "donnees_filtrees_chat.json")

    # Affichage final
    print("\n📌 Aperçu de 5 organisations filtrées :")
    for org in donnees_filtrees[:5]:
        print(json.dumps(org, indent=4))


# Lancer la pipeline
if __name__ == "__main__":
    main()
