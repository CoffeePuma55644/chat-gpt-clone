import requests  # Importation de la librairie pour effectuer des requêtes HTTP
import os        # Importation de la librairie pour interagir avec le système d'exploitation

# Récupère la clé API stockée dans les variables d'environnement
api_key = os.getenv("MIMO_OPENAI_API_KEY")
# URL de l'API de Mimo
url = "https://ai.mimo.org/v1/openai/message"
# Prépare les en-têtes HTTP en incluant la clé API
headers = {"api-key": api_key}

# Fonction pour envoyer un message à l'API de Mimo
def send_message(user_message, thread_id):
    # Prépare le corps de la requête avec le message de l'utilisateur
    body = {"message": user_message}
    # Si un identifiant de thread est fourni, l'ajoute au corps de la requête
    if thread_id:
        body["threadId"] = thread_id
    # Envoie une requête POST à l'API avec les en-têtes et le corps encodé en JSON
    response = requests.post(url, headers=headers, json=body)
    # Retourne la réponse de l'API convertie en dictionnaire Python
    return response.json()

# Initialise l'identifiant du thread courant à None (aucun thread au départ)
current_thread_id = None

# Affiche le message de bienvenue et les instructions pour l'utilisateur
print("Bienvenu dans le CoffeePumaGPT ! Entre ton ptn de message vsy")
print("Pour quitter fait 'exit' slm...")
print("Pour le nouveau thread fait 'new'...")

# Boucle principale pour gérer l'interaction avec l'utilisateur
while True:
    # Demande à l'utilisateur d'entrer son message
    user_message = input("Toi: ")

    # Si l'utilisateur tape "exit", on quitte le programme
    if user_message == "exit":
        print("Fin du programme")
        break

    # Si l'utilisateur tape "new", on réinitialise le thread courant pour démarrer un nouveau fil de discussion
    elif user_message == "new":
        current_thread_id = None
        print("Un nouveau thread commence")
        continue

    # Sinon, on envoie le message à l'API via la fonction send_message
    else:
        response_data = send_message(user_message, current_thread_id)
        # Récupère le message de réponse renvoyé par l'API
        latest_message = response_data.get("response")
        # Met à jour l'identifiant du thread avec celui fourni par l'API
        current_thread_id = response_data.get("threadId")
        # Affiche la réponse de l'API
        print(f"GPT: {latest_message}")

# Création d'une liste pour stocker les threads (bien que dans ce code, elle n'est pas vraiment utilisée)
threads = []
threads.append(current_thread_id)
