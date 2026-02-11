# test_openai.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Charger la clé API depuis le fichier .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérification simple que la clé est chargée
if not OPENAI_API_KEY:
    print("❌ ERREUR : La clé API OpenAI n'a pas été trouvée dans .env")
    print("   Vérifiez que votre fichier .env contient: OPENAI_API_KEY=votre_clé")
    exit(1)

print(f"✅ Clé API OpenAI chargée : OUI ({len(OPENAI_API_KEY)} caractères)")

# 2. Initialiser le client OpenAI
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # 3. Faire un test simple avec GPT-3.5-Turbo
    print("🔄 Envoi de la requête à l'API OpenAI...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Explique-moi comment fonctionne l'IA en une phrase."}
        ],
        max_tokens=100
    )
    
    # 4. Afficher la réponse
    print("✅ Réponse reçue avec succès !")
    print("\n" + "="*50)
    print("RÉPONSE D'OPENAI:")
    print("="*50)
    print(response.choices[0].message.content)
    print("="*50)
    
except Exception as e:
    print(f"❌ Une erreur s'est produite : {type(e).__name__}")
    print(f"   Détails : {str(e)}")