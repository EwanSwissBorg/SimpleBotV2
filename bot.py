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
(
    PROJECT_NAME, 
    TOKEN_TICKER, 
    ELEVATOR_PITCH, 
    PROBLEM_SOLVING, 
    SOLUTION, 
    TECHNOLOGY, 
    TARGET_MARKET, 
    GROWTH_STRATEGY, 
    COMPETITORS, 
    DIFFERENTIATORS, 
    TOKEN_METRICS, 
    VESTING_SCHEDULE, 
    ROADMAP, 
    TEAM_INFO, 
    ESSENTIAL_LINKS, 
    ADDITIONAL_INFO
) = range(16)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Gm! 👋 I'm the BorgPad Curator Bot. I'll help you create a professional data room "
        "for your project. Let's start with your basic Project Information.\n\n"
        "What is your project name? 🏷️"
    )
    return PROJECT_NAME

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
    await update.message.reply_text("Let's Deep dive more into your project now!\n\n"
                                      "Point 1/7: What's the main problem you're solving? ❓")
    return PROBLEM_SOLVING

async def handle_problem_solving(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['problem_solving'] = update.message.text
    await update.message.reply_text("Point 2/7: What's your solution? 💡")
    return SOLUTION

async def handle_solution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['solution'] = update.message.text
    await update.message.reply_text("Point 3/7: How does your technology work? ⚙️")
    return TECHNOLOGY

async def handle_technology(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['technology'] = update.message.text
    await update.message.reply_text("Point 4/7: Who is your target market? 🎯")
    return TARGET_MARKET

async def handle_target_market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['target_market'] = update.message.text
    await update.message.reply_text("Point 5/7: What's your growth strategy? 📈")
    return GROWTH_STRATEGY

async def handle_growth_strategy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['growth_strategy'] = update.message.text
    await update.message.reply_text("Point 6/7: Who are your main competitors in the market? 🔍")
    return COMPETITORS

async def handle_competitors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['competitors'] = update.message.text
    await update.message.reply_text("Point 7/7: What are your key differentiators? List 3-5 points that set you apart 💪")
    return DIFFERENTIATORS

async def handle_differentiators(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['differentiators'] = update.message.text
    await update.message.reply_text("Let's jump into the tokenomics part! 📊\n\n"
                                      "Token Metrics (give the example of the format you need : 1,000,000,000)\n"
                                      "• Total Supply 📊")
    return TOKEN_METRICS

async def handle_token_metrics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['token_metrics'] = update.message.text
    await update.message.reply_text("List each category with its percentage using this format: 'XX% - Category Name'. "
                                      "Don't forget to include the percent for your initial liquidity pool that will be burned! 🔥")
    return VESTING_SCHEDULE

async def handle_vesting_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['vesting_schedule'] = update.message.text
    await update.message.reply_text("Project Roadmap & Team 🗺️\n\n"
                                      "Please outline your quarterly roadmap for the next 6-12 months. "
                                      "For each quarter, list 2-3 key objectives in bullet points.")
    return ROADMAP

async def handle_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['roadmap'] = update.message.text
    await update.message.reply_text("Team Information 👥\n\n"
                                      "For each key team member, provide:\n"
                                      "• Name and position\n"
                                      "• LinkedIn link (if available)\n"
                                      "• X/Twitter link (if available)")
    return TEAM_INFO

async def handle_team_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['team_info'] = update.message.text
    await update.message.reply_text("Essential Links 🔗\n\n"
                                      "• Pitch deck URL 📑\n"
                                      "• Community chat (Telegram/Discord) 💬\n"
                                      "• Website URL 🌐\n"
                                      "If you want to add another important link add:\n"
                                      "- Name_Link link")
    return ESSENTIAL_LINKS

async def handle_essential_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['essential_links'] = update.message.text
    await update.message.reply_text("Additional Information 📝\n\n"
                                      "9. Launch Strategy & Vision\n"
                                      "• Why have you chosen to pursue a DEX-only launch? 🤔\n"
                                      "• Do you have a powerful quote from a founder or notable personality about your project? "
                                      "Please include their name and title 💭")
    return ADDITIONAL_INFO

async def handle_additional_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['additional_info'] = update.message.text
    await summary(update, context)  # Appel de la fonction summary ici
    return ConversationHandler.END

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    recap = (
        "🎉 Here's a summary of your project submission:\n\n"
        f"Project Name: {context.user_data['project_name']} 🏷️\n"
        f"Token Ticker: {context.user_data['token_ticker']} 💎\n"
        f"Elevator Pitch: {context.user_data['elevator_pitch']} 🚀\n"
        f"Main Problem: {context.user_data['problem_solving']} ❓\n"
        f"Solution: {context.user_data['solution']} 💡\n"
        f"Technology: {context.user_data['technology']} ⚙️\n"
        f"Target Market: {context.user_data['target_market']} 🎯\n"
        f"Growth Strategy: {context.user_data['growth_strategy']} 📈\n"
        f"Competitors: {context.user_data['competitors']} 🔍\n"
        f"Differentiators: {context.user_data['differentiators']} 💪✨\n"
        f"Token Metrics: {context.user_data['token_metrics']} 📊\n"
        f"Vesting Schedule: {context.user_data['vesting_schedule']} ⏳\n"
        f"Roadmap: {context.user_data['roadmap']} 🗺️\n"
        f"Team Info: {context.user_data['team_info']} 👥\n"
        f"Essential Links: {context.user_data['essential_links']} 🔗\n"
        f"Additional Info: {context.user_data['additional_info']} 📝\n\n"
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
            PROBLEM_SOLVING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_problem_solving)],
            SOLUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solution)],
            TECHNOLOGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_technology)],
            TARGET_MARKET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_market)],
            GROWTH_STRATEGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_growth_strategy)],
            COMPETITORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_competitors)],
            DIFFERENTIATORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_differentiators)],
            TOKEN_METRICS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_metrics)],
            VESTING_SCHEDULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vesting_schedule)],
            ROADMAP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roadmap)],
            TEAM_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_team_info)],
            ESSENTIAL_LINKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_essential_links)],
            ADDITIONAL_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_additional_info)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()