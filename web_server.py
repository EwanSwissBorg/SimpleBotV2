from flask import Flask, request, redirect
import tweepy
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

app = Flask(__name__)

def setup_twitter_auth():
    callback_url = os.getenv("CALLBACK_URL")
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        callback_url
    )
    return auth

@app.route('/callback')
def twitter_callback():
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')
    
    print(f"Received oauth_token: {oauth_token}")
    
    try:
        auth = setup_twitter_auth()
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