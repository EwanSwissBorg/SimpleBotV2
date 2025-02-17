from flask import Flask, request, redirect
import tweepy
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

app = Flask(__name__)

# Stockage temporaire en mémoire (attention: ceci n'est pas idéal pour la production)
temp_tokens = {}

def setup_twitter_auth():
    callback_url = os.getenv("CALLBACK_URL")
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        callback_url
    )
    return auth

@app.route('/start_auth')
def start_auth():
    auth = setup_twitter_auth()
    try:
        redirect_url = auth.get_authorization_url()
        # Stocker le request_token temporairement
        temp_tokens[auth.request_token['oauth_token']] = auth.request_token
        return redirect(redirect_url)
    except Exception as e:
        return f"Erreur lors de l'authentification : {str(e)}"

@app.route('/callback')
def twitter_callback():
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')
    
    print(f"Received oauth_token: {oauth_token}")
    
    try:
        # Récupérer le request_token stocké
        request_token = temp_tokens.get(oauth_token)
        if not request_token:
            return "Token non trouvé"
        
        auth = setup_twitter_auth()
        auth.request_token = request_token
        
        auth.get_access_token(oauth_verifier)
        api = tweepy.API(auth)
        user = api.verify_credentials()
        
        # Nettoyer le token utilisé
        temp_tokens.pop(oauth_token, None)
        
        return redirect(f"https://t.me/simpleewanv2bot?start=auth_success_{user.screen_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Erreur détaillée : {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 