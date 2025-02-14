from telegram import Update
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

load_dotenv()

# Définition des états de la conversation
PROJECT_NAME, TOKEN_TICKER, ELEVATOR_PITCH = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Gm! 👋 I'm the BorgPad Curator Bot. I'll help you create a professional data room "
        "for your project. I'll ask you a series of questions to gather all the necessary "
        "information. Let's start with your basic Project Information.\n\n"
        "What is your project name? 🏷️"
    )
    return PROJECT_NAME  # Retourne l'état pour la prochaine question

async def handle_project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("Great! Now, what is your token ticker? 💎")
    return TOKEN_TICKER

async def handle_token_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['token_ticker'] = update.message.text
    await update.message.reply_text("What is your elevator pitch? 🚀")
    return ELEVATOR_PITCH

async def handle_elevator_pitch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['elevator_pitch'] = update.message.text
    await summary(update, context)  # Appel de la fonction summary ici
    return ConversationHandler.END  # Termine la conversation

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    recap = (
        "🎉 Here's a summary of your project submission:\n\n"
        f"Project Name: {context.user_data['project_name']} 🏷️\n"
        f"Token Ticker: {context.user_data['token_ticker']} 💎\n"
        f"Elevator Pitch: {context.user_data['elevator_pitch']} 🚀\n\n"
        "✨ Thank you for submitting your project to BorgPad! ✨"
    )
    
    await update.message.reply_text(recap)

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_project_name)],
            TOKEN_TICKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_ticker)],
            ELEVATOR_PITCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_elevator_pitch)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()