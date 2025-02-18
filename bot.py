from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import tweepy
from database import init_db, save_project_data  # Ajoutez cet import
import re
from datetime import datetime
from PIL import Image
load_dotenv()

# Définition des états de la conversation
(
    USERNAME,
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    PROJECT_PICTURE,
    WEBSITE_LINK,
    COMMUNITY_LINK,
    X_LINK,
    DEPLOY_CHAIN,
    SECTOR,
    TGE_DATE,
    FDV,
    TOKEN_TICKER,
    DATA_ROOM,
    TOKEN_PICTURE
) = range(14)

def setup_twitter_auth():
    callback_url = os.getenv("CALLBACK_URL")
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        callback_url
    )
    return auth

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Vérifier si c'est un retour d'authentification Twitter
    message_text = update.message.text if update.message else None
    if not message_text:
        return ConversationHandler.END

    print(f"Received message: {message_text}")  # Debug log

    if message_text.startswith("/start auth_success_"):
        username = message_text.replace("/start auth_success_", "")
        context.user_data['username'] = username
        
        # Display the website example image
        with open('website_example.png', 'rb') as image:
            await update.message.reply_photo(photo=image, caption=f"Welcome {username}! 👋\n\n"
            "I'm the BorgPad Curator Bot. I'll help you to create your commitment page on BorgPad as the image above.\n\n"
            "1/13 - What is your project name? 🏷️"
        )
        return PROJECT_NAME

    # Si ce n'est pas un retour d'auth, procéder avec l'authentification Twitter
    try:
        # Utiliser directement l'URL de start_auth
        auth_url = f"{os.getenv('CALLBACK_URL').rsplit('/', 1)[0]}/start_auth"
        print(f"Auth URL: {auth_url}")  # Debug log
        
        keyboard = [[InlineKeyboardButton("Connect with Twitter", url=auth_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Gm! 👋 I'm the BorgPad Curator Bot.\n\n"
            "Please connect your Twitter account to continue:",
            reply_markup=reply_markup
        )
        return USERNAME
    except Exception as e:
        print(f"Error in start: {str(e)}")  # Debug log
        await update.message.reply_text(f'Error during Twitter authentication: {str(e)}')
        return ConversationHandler.END

async def handle_project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("2/13 - One sentence to describe your project 💎")
    return PROJECT_DESCRIPTION

async def handle_project_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['project_description'] = update.message.text
    await update.message.reply_text("3/13 - Send your project picture in jpg or png format 🖼️ (WITH COMPRESSION - so please ensure a high quality image first)")
    return PROJECT_PICTURE

async def handle_project_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    print("update.message", update.message)
    # Vérifier si le message est un texte
    if update.message.text:
        await update.message.reply_text("Please send a picture in jpg or png format with compression 🖼️")
        return PROJECT_PICTURE

    # Vérifier si un fichier photo a été envoyé
    if not update.message.photo:
        await update.message.reply_text("Please send a picture in jpg or png format with compression 🖼️")
        return PROJECT_PICTURE
    
    try:
        print("Received photo")
        # Obtenir le fichier photo avec la meilleure qualité
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        # Créer le dossier 'project_pictures' s'il n'existe pas
        if not os.path.exists('project_pictures'):
            os.makedirs('project_pictures')
        
        # Générer un nom de fichier unique
        file_name = f"project_pictures/{context.user_data['username']}_{photo.file_unique_id}.jpg"
        
        # Télécharger la photo
        await photo_file.download_to_drive(file_name)
        
        # Vérifier si le fichier est un JPG ou PNG
        if not is_valid_image(file_name):
            await update.message.reply_text("The file is not a valid image format. Please send a JPG or PNG file.")
            return PROJECT_PICTURE
        
        # Sauvegarder le chemin de l'image dans les données utilisateur
        context.user_data['project_picture'] = file_name
        
        await update.message.reply_text("4/13 - Your website Link 🌐")
        return WEBSITE_LINK
        
    except Exception as e:
        print(f"Error handling project picture: {str(e)}")
        await update.message.reply_text("❌ An error occurred while processing your picture. Please try again.")
        return PROJECT_PICTURE

async def handle_website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['website_link'] = update.message.text
    await update.message.reply_text("5/13 - Your telegram OR discord link (your main channel to communicate your community) 💬")
    return COMMUNITY_LINK

async def handle_community_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['community_link'] = update.message.text
    await update.message.reply_text("6/13 - Your X link 🐦")
    return X_LINK

async def handle_x_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['x_link'] = update.message.text
    await update.message.reply_text("7/13 - On which chain you want to deploy? ⛓️")
    return DEPLOY_CHAIN

async def handle_deploy_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['deploy_chain'] = update.message.text
    await update.message.reply_text("8/13 - What is your sector? 🎯 (Depin / SocialFi / DeFi etc.)")
    return SECTOR

async def handle_sector(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['sector'] = update.message.text
    
    # Créer les boutons pour la TGE date
    keyboard = [
        [InlineKeyboardButton("1 to 2 weeks", callback_data="tge_1-2weeks")],
        [InlineKeyboardButton("1 month to 2 months", callback_data="tge_1-2months")],
        [InlineKeyboardButton("more than 2 months", callback_data="tge_2months+")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "9/13 - When do you plan to do your TGE? 📅",
        reply_markup=reply_markup
    )
    return TGE_DATE

async def handle_tge_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    # Extraire la valeur de TGE date du callback_data
    tge_value = query.data.replace("tge_", "")
    context.user_data['tge_date'] = tge_value

    # Informer l'utilisateur de la TGE choisie
    await query.message.reply_text(f"TGE selected: {tge_value} 📅")
    
    # Créer les boutons pour la FDV
    keyboard = [
        [InlineKeyboardButton("1M to 5M", callback_data="fdv_1-5M")],
        [InlineKeyboardButton("5M to 10M", callback_data="fdv_5-10M")],
        [InlineKeyboardButton("10M to 25M", callback_data="fdv_10-25M")],
        [InlineKeyboardButton("25M to 50M", callback_data="fdv_25-50M")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        text="10/13 - What is your target FDV? 💰",
        reply_markup=reply_markup
    )
    return FDV

async def handle_fdv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    # Extraire la valeur de FDV du callback_data
    fdv_value = query.data.replace("fdv_", "")
    context.user_data['fdv'] = fdv_value
    
    await query.edit_message_text(
        text=f"FDV selected: {fdv_value} 💰"
    )
    
    await query.message.reply_text(
        "11/13 - Your token TICKER $XXXXX 🎫 (must start with '$' and be up to 5 characters long in uppercase)"
    )
    
    return TOKEN_TICKER

def is_valid_fdv(fdv: str) -> bool:
    return fdv.isdigit() and int(fdv) > 0

async def handle_token_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ticker = update.message.text
    
    if not is_valid_ticker(ticker):
        await update.message.reply_text("11/13 - Please enter a valid token ticker (must start with '$' and be up to 5 characters long in uppercase). 💔")
        return TOKEN_TICKER
    
    context.user_data['token_ticker'] = ticker
    await update.message.reply_text("12/13 - Send your token picture in jpg or png format 🖼️ (WITH COMPRESSION - so please ensure a high quality image first)")
    return TOKEN_PICTURE

def is_valid_ticker(ticker: str) -> bool:
    return ticker.startswith('$') and len(ticker) <= 6 and len(ticker) >= 2 and ticker[1:].isupper()

async def handle_token_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Vérifier si le message est un texte
    if update.message.text:
        await update.message.reply_text("Please send a picture in jpg or png format with compression 🖼️")
        return TOKEN_PICTURE

    # Vérifier si un fichier photo a été envoyé
    if not update.message.photo:
        await update.message.reply_text("Please send a picture in jpg or png format with compression 🖼️")
        return TOKEN_PICTURE
    
    try:
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        if not os.path.exists('token_pictures'):
            os.makedirs('token_pictures')
        
        file_name = f"token_pictures/{context.user_data['username']}_{photo.file_unique_id}.jpg"
        await photo_file.download_to_drive(file_name)
        
        # Vérifier si le fichier est un JPG ou PNG
        if not is_valid_image(file_name):
            await update.message.reply_text("The file is not a valid image format. Please send a JPG or PNG file.")
            return TOKEN_PICTURE
        
        context.user_data['token_picture'] = file_name
        
        await update.message.reply_text(
            "13/13 - To provide the most information to your investors - and make them want to invest - you need a data room 📚\n\n"
            "Examples:\n"
            "Ambient: https://borgpad-data-room.notion.site/moemate?pvs=4\n"
            "Solana ID: https://www.solana.id/solid\n\n"
            "Here is a template: https://docs.google.com/document/d/1j3hxzO8_9wNfWfVxGNRDLFV8TJectQpX4bY6pSxCLGs/edit?tab=t.0\n\n"
            "Share the link of your data room 📝"
        )
        return DATA_ROOM
        
    except Exception as e:
        print(f"Error handling token picture: {str(e)}")
        await update.message.reply_text("❌ An error occurred while processing your picture. Please try again.")
        return TOKEN_PICTURE

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format in ['JPEG', 'PNG']
    except Exception:
        return False

async def handle_data_room(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['data_room'] = update.message.text
    
    # Préparer le résumé final
    summary_message = (
        "🎉 Here is a summary of your project:\n\n"
        f"👤 Username: {context.user_data['username']}\n"
        f"🏷️ Project Name: {context.user_data['project_name']}\n"
        f"💎 Project Description: {context.user_data['project_description']}\n"
        f"🖼️ Project Picture: Saved successfully\n"
        f"🌐 Website Link: {context.user_data['website_link']}\n"
        f"💬 Community Link: {context.user_data['community_link']}\n"
        f"🐦 X Link: {context.user_data['x_link']}\n"
        f"⛓️ Deploy Chain: {context.user_data['deploy_chain']}\n"
        f"🎯 Sector: {context.user_data['sector']}\n"
        f"📅 TGE Date: {context.user_data['tge_date']}\n"
        f"💰 FDV: {context.user_data['fdv']}\n"
        f"🎫 Token Ticker: {context.user_data['token_ticker']}\n"
        f"🖼️ Token Picture: Saved successfully\n"
        f"📚 Data Room: {context.user_data['data_room']}"
    )
    
    try:
        save_project_data(context.user_data)
        # Envoyer le résumé avec la dernière image (project picture)
        with open(context.user_data['project_picture'], 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=summary_message
            )
        await update.message.reply_text("✅ Your information has been successfully saved!")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        await update.message.reply_text("❌ An error occurred while saving your data.")
    
    return ConversationHandler.END

def main():
    # Initialiser la base de données
    init_db()
    
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [
                CommandHandler('start', start),
                MessageHandler(filters.TEXT & ~filters.COMMAND, start)
            ],
            PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_name)],
            PROJECT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_description)],
            PROJECT_PICTURE: [
                MessageHandler(filters.PHOTO, handle_project_picture),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_picture)
            ],
            WEBSITE_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_website_link)],
            COMMUNITY_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_community_link)],
            X_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_x_link)],
            DEPLOY_CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_deploy_chain)],
            SECTOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sector)],
            TGE_DATE: [CallbackQueryHandler(handle_tge_date, pattern=r"^tge_")],
            FDV: [CallbackQueryHandler(handle_fdv, pattern=r"^fdv_")],
            TOKEN_TICKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_ticker)],
            TOKEN_PICTURE: [
                MessageHandler(filters.PHOTO, handle_token_picture),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_picture)
            ],
            DATA_ROOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_data_room)],
        },
        fallbacks=[],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()