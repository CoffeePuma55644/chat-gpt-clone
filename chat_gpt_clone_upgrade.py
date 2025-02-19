import requests
import os

def send_message(user_message, thread_id=None):
    """
    Envoie un message à l'API de Mimo et retourne la réponse sous forme de dictionnaire.
    
    Args:
        user_message (str): Le message de l'utilisateur.
        thread_id (str, optionnel): L'ID du thread en cours, None par défaut.
    
    Returns:
        dict: La réponse JSON convertie en dictionnaire. En cas d'erreur, retourne un dictionnaire vide.
    """
    # Construction du payload de la requête
    payload = {"message": user_message}
    if thread_id:
        payload["threadId"] = thread_id

    # Récupère la clé API depuis les variables d'environnement
    api_key = os.getenv("MIMO_OPENAI_API_KEY")
    if not api_key:
        print("Erreur : Clé API 'MIMO_OPENAI_API_KEY' non trouvée.")
        return {}
    
    # Définit l'URL de l'API et les en-têtes contenant la clé API
    url = "https://ai.mimo.org/v1/openai/message"
    headers = {"api-key": api_key}
    
    try:
        # Envoie la requête POST et vérifie si la réponse est correcte
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        return response.json()       # Retourne le contenu JSON converti en dict
    except requests.exceptions.RequestException as e:
        # Affiche l'erreur et retourne un dictionnaire vide en cas d'exception
        print(f"Erreur lors de la requête API: {e}")
        return {}

def main():
    """
    Fonction principale qui gère l'interaction avec l'utilisateur et le dialogue avec l'API.
    """
    current_thread_id = None  # Initialise l'ID du thread courant
    print("Bienvenue dans le MokoliGPT !")
    print("Tape 'exit' pour quitter, 'new' pour démarrer un nouveau thread.")
    
    while True:
        # Lecture et nettoyage de la saisie utilisateur
        user_message = input("Toi: ").strip()
        
        # Commande pour quitter le programme
        if user_message.lower() == "exit":
            print("Fin du programme. À bientôt !")
            break
        
        # Commande pour démarrer un nouveau thread
        if user_message.lower() == "new":
            current_thread_id = None
            print("Nouveau thread démarré.")
            continue
        
        # Envoie le message à l'API et récupère la réponse
        response_data = send_message(user_message, current_thread_id)
        if not response_data:
            # En cas d'erreur dans la réponse, on passe au prochain tour de boucle
            continue
        
        # Récupère le message de réponse et met à jour l'ID du thread
        latest_message = response_data.get("response", "Aucune réponse reçue")
        current_thread_id = response_data.get("threadId", current_thread_id)
        print(f"GPT: {latest_message}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Permet une sortie propre si l'utilisateur interrompt le programme (Ctrl+C)
        print("\nProgramme interrompu par l'utilisateur.")
