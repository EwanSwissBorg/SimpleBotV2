from flask import Flask, request, redirect
import tweepy
import os
from dotenv import load_dotenv
import redis
import json
from telegram import Bot

load_dotenv()

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialiser le bot Telegram
telegram_bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

def setup_twitter_auth():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("CALLBACK_URL")
    )
    return auth

@app.route('/callback')
def twitter_callback():
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')
    
    print(f"Received oauth_token: {oauth_token}")
    stored_token = redis_client.get(oauth_token)
    print(f"Stored token from Redis: {stored_token}")
    
    if not stored_token:
        return f"Token {oauth_token} non trouvé dans Redis"
    
    try:
        request_token = json.loads(stored_token)
        print(f"Decoded request_token: {request_token}")
        
        auth = setup_twitter_auth()
        auth.request_token = request_token
        
        auth.get_access_token(oauth_verifier)
        api = tweepy.API(auth)
        user = api.verify_credentials()
        
        # Redirection vers le nouveau bot Telegram
        return redirect(f"https://t.me/simpleewanv2bot?start=auth_success_{user.screen_name}")
        
    except Exception as e:
        return f"Erreur détaillée : {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 