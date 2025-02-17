from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import tweepy
from database import init_db, save_project_data  # Ajoutez cet import
import requests
from datetime import datetime

load_dotenv()

# Définition des états de la conversation
(
    USERNAME,
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    WEBSITE_LINK,
    COMMUNITY_LINK,
    X_LINK,
    DEPLOY_CHAIN,
    SECTOR,
    TGE_DATE,
    FDV,
    TOKEN_TICKER,
    DATA_ROOM
) = range(12)

def setup_twitter_auth():
    callback_url = os.getenv("CALLBACK_URL")
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        callback_url
    )
    return auth

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message_text = update.message.text if update.message else None
    if not message_text:
        return ConversationHandler.END

    print(f"Received message: {message_text}")  # Debug log

    if message_text.startswith("/start auth_success_"):
        username = message_text.replace("/start auth_success_", "")
        context.user_data['username'] = username
        print(f"Authenticated user: {username}")  # Debug log
        await update.message.reply_text(
            f"Welcome {username}! 👋\n\n"
            "I'm the BorgPad Curator Bot. I'll help you create a professional data room "
            "for your project.\n\n"
            "What is your project name? 🏷️"
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
    await update.message.reply_text("Great! Now, what is your token ticker? 💎")
    return TOKEN_TICKER

async def handle_token_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ticker = update.message.text
    
    if not is_valid_ticker(ticker):
        await update.message.reply_text("Please enter a valid token ticker (must start with '$' and be up to 5 characters long). 💔")
        return TOKEN_TICKER  # Stay in the same state to ask for the ticker again
    
    context.user_data['token_ticker'] = ticker
    await update.message.reply_text("What is your elevator pitch? 🚀")
    return ELEVATOR_PITCH

def is_valid_ticker(ticker: str) -> bool:
    return ticker.startswith('$') and len(ticker) <= 6 and len(ticker) >= 2 and ticker[1:].isupper()  # Check if it starts with '$', is up to 5 characters long, and is uppercase

async def handle_project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("One sentence to describe your project:")
    return PROJECT_DESCRIPTION

async def handle_project_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['project_description'] = update.message.text
    await update.message.reply_text("Your website Link:")
    return WEBSITE_LINK

async def handle_website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['website_link'] = update.message.text
    await update.message.reply_text("Your telegram / discord link (your main channel to communicate your community):")
    return COMMUNITY_LINK

async def handle_community_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['community_link'] = update.message.text
    await update.message.reply_text("Your X link:")
    return X_LINK

async def handle_x_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['x_link'] = update.message.text
    await update.message.reply_text("On which chain you want to deploy?")
    return DEPLOY_CHAIN

async def handle_deploy_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['deploy_chain'] = update.message.text
    await update.message.reply_text("What is your sector?")
    return SECTOR

async def handle_sector(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['sector'] = update.message.text
    await update.message.reply_text("On which date you want to TGE? (DD/MM/YYYY)")
    return TGE_DATE

async def handle_tge_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Vérifier le format de la date
    date_text = update.message.text
    try:
        datetime.strptime(date_text, '%d/%m/%Y')
        context.user_data['tge_date'] = date_text
        await update.message.reply_text("At which FDV?")
        return FDV
    except ValueError:
        await update.message.reply_text("Please enter the date in DD/MM/YYYY format:")
        return TGE_DATE

async def handle_fdv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['fdv'] = update.message.text
    await update.message.reply_text("Your token TICKER %XXXXX:")
    return TOKEN_TICKER

async def handle_token_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ticker = update.message.text
    if not ticker.startswith('%') or len(ticker) > 6:
        await update.message.reply_text("Please enter a valid token ticker (must start with '%' and be up to 5 characters long):")
        return TOKEN_TICKER
    
    context.user_data['token_ticker'] = ticker
    await update.message.reply_text(
        "To provide the most information to your investors - and make them want to invest - you need a data room:\n"
        "Examples:\n"
        "Ambient: https://borgpad-data-room.notion.site/moemate?pvs=4\n"
        "Solana ID: https://www.solana.id/solid\n"
        "Here is a template: https://docs.google.com/document/d/1j3hxzO8_9wNfWfVxGNRDLFV8TJectQpX4bY6pSxCLGs/edit?tab=t.0\n\n"
        "Share the link of your data room:"
    )
    return DATA_ROOM

async def handle_data_room(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['data_room'] = update.message.text
    
    # Ici vous pouvez ajouter la logique pour sauvegarder toutes les données collectées
    try:
        save_project_data(context.user_data)
        await update.message.reply_text("✅ Your information has been successfully saved!")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        await update.message.reply_text("❌ An error occurred while saving your data.")
    
    return ConversationHandler.END

def create_pie_chart(token_distribution: str) -> str:
    # Parse the token distribution
    categories = []
    percentages = []
    
    lines = token_distribution.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split('-')
        if len(parts) == 2:
            percentage_part = parts[0].strip()
            category_part = parts[1].strip()
            if percentage_part.endswith('%'):
                percentage = int(percentage_part[:-1])  # Remove '%' and convert to int
                categories.append(category_part)
                percentages.append(percentage)

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Token Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart as an image
    chart_path = 'token_distribution_chart.png'
    plt.savefig(chart_path)
    plt.close()  # Close the plot to free memory

    return chart_path

def create_cumulative_emission_graph(vesting_schedule_details: list, token_distribution: dict) -> str:
    # Determine maximum months needed for the graph
    max_total_months = 0
    for category_with_percentage, details in vesting_schedule_details:
        cliff_months = details[0]
        linear_vesting_months = details[2]
        total_months = cliff_months + linear_vesting_months
        max_total_months = max(max_total_months, total_months)
    
    max_total_months += 5  # Add buffer for visualization
    emissions_by_category = {}
    
    # Process each category
    for category_with_percentage, details in vesting_schedule_details:
        category, percentage_str = category_with_percentage.split('(')
        category = category.strip()
        percentage = float(percentage_str.strip(' %)'))
        
        cliff_months = details[0]
        initial_unlock = details[1]
        linear_vesting_months = details[2]
        
        emissions = np.zeros(max_total_months + 1)
        
        # Initial unlock at TGE (month 0)
        if initial_unlock > 0:
            emissions[0] = percentage * (initial_unlock / 100)
        
        remaining_amount = percentage * (1 - initial_unlock / 100)
        
        if linear_vesting_months > 0:
            monthly_emission = remaining_amount / linear_vesting_months
            
            # Apply linear vesting after cliff period
            for month in range(cliff_months + 1, cliff_months + linear_vesting_months + 1):
                if month <= max_total_months:
                    emissions[month] = monthly_emission
        else:
            # If no linear vesting, release remaining tokens after cliff
            if cliff_months < max_total_months:
                emissions[cliff_months] = remaining_amount
        
        emissions = np.cumsum(emissions)
        emissions_by_category[category] = {
            'emissions': emissions,
            'cliff_months': cliff_months,
            'initial_unlock': initial_unlock,
            'percentage': percentage,
            'total_months': cliff_months + linear_vesting_months
        }

    plt.figure(figsize=(12, 8))
    
    colors = {
        'Team': 'salmon',
        'Advisors': 'mediumpurple',
        'Liquidity': 'lightgreen',
        'Marketing': 'pink',
        'Development': 'lightblue',
        'Treasury': 'plum',
        'Ecosystem': 'mediumseagreen',
        'Private': 'orange',
        'Public': 'yellow',
        'Partners': 'cyan',
        'Community': 'lightgray'
    }
    
    x = np.arange(max_total_months + 1)
    bottom = np.zeros(max_total_months + 1)
    
    # Sort by total vesting duration (ascending) and initial unlock (descending)
    sorted_categories = sorted(
        emissions_by_category.items(),
        key=lambda x: (x[1]['total_months'], -x[1]['initial_unlock'])
    )
    
    # Plot each category
    for category, data in sorted_categories:
        plt.fill_between(x, bottom, bottom + data['emissions'],
                        label=f"{category} ({data['percentage']}%)",
                        color=colors.get(category, None),
                        alpha=0.6)
        bottom += data['emissions']

    # Customize the plot
    plt.title('Cumulative Token Emission Schedule', fontsize=14, pad=20)
    plt.xlabel('Months', fontsize=12)
    plt.ylabel('Cumulative Tokens in Circulation (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Token Categories', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Set axis limits
    plt.xlim(0, max_total_months)
    plt.ylim(0, 100)
    
    # Adjust layout
    plt.tight_layout()

    # Save and return
    graph_path = 'cumulative_emission_graph.png'
    plt.savefig(graph_path, bbox_inches='tight', dpi=300)
    plt.close()

    return graph_path

def parse_token_distribution(token_distribution: str) -> dict:
    distribution = {}
    
    # Split the input by lines
    lines = token_distribution.splitlines()
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        # Split by the '-' character
        parts = line.split('-')
        if len(parts) != 2:
            print(f"Invalid format for line: {line}")
            continue  # Skip invalid lines
        
        percentage_part = parts[0].strip()
        category_part = parts[1].strip()

        # Extract the percentage and convert to integer
        if percentage_part.endswith('%'):
            percentage = int(percentage_part[:-1])  # Remove '%' and convert to int
            distribution[category_part] = percentage
        else:
            print(f"Invalid percentage format for line: {line}")

    return distribution

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Diviser le récapitulatif en plusieurs messages plus petits
    part1 = (
        "🎉 Here's a summary of your project submission (Part 1/3):\n\n"
        f"Project Name: {context.user_data['project_name']} 🏷️\n"
        f"Token Ticker: {context.user_data['token_ticker']} 💎\n"
        f"Project Description: {context.user_data['project_description']} 📝\n"
        f"Website Link: {context.user_data['website_link']} 🌐\n"
        f"Community Link: {context.user_data['community_link']} 💬\n"
        f"X Link: {context.user_data['x_link']} 🔗\n"
        f"Deploy Chain: {context.user_data['deploy_chain']} 🔗\n"
        f"Sector: {context.user_data['sector']} 📊\n"
        f"TGE Date: {context.user_data['tge_date']} 📅\n"
        f"FDV: {context.user_data['fdv']} 💰\n"
    )

    part2 = (
        "🎉 Project Summary (Part 2/3):\n\n"
        f"Data Room: {context.user_data['data_room']} 📁\n"
    )

    part3 = (
        "🎉 Project Summary (Part 3/3):\n\n"
        "✨ Thank you for submitting your project to BorgPad! ✨"
    )
    
    # Envoyer chaque partie séparément
    await update.message.reply_text(part1)
    await update.message.reply_text(part2)
    await update.message.reply_text(part3)

    # Créer et envoyer les graphiques
    chart_path = create_pie_chart(context.user_data['data_room'])
    with open(chart_path, 'rb') as chart_file:
        await update.message.reply_photo(photo=chart_file)

    return ConversationHandler.END

def main():
    # Initialiser la base de données
    init_db()
    
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, start)],
            PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_name)],
            PROJECT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_description)],
            WEBSITE_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_website_link)],
            COMMUNITY_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_community_link)],
            X_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_x_link)],
            DEPLOY_CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_deploy_chain)],
            SECTOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sector)],
            TGE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tge_date)],
            FDV: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_fdv)],
            TOKEN_TICKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_ticker)],
            DATA_ROOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_data_room)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()