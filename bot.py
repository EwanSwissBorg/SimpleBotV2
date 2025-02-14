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
import matplotlib.pyplot as plt
import numpy as np
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
    INITIAL_SUPPLY,
    TARGET_FDV,
    TOKEN_DISTRIBUTION,
    VESTING_SCHEDULE,
    ROADMAP, 
    TEAM_INFO, 
    ESSENTIAL_LINKS,
    ADDITIONAL_INFO,
    DEX_INFO
) = range(20)

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
    ticker = update.message.text
    
    if not is_valid_ticker(ticker):
        await update.message.reply_text("Please enter a valid token ticker (must start with '$' and be up to 5 characters long). 💔")
        return TOKEN_TICKER  # Stay in the same state to ask for the ticker again
    
    context.user_data['token_ticker'] = ticker
    await update.message.reply_text("What is your elevator pitch? 🚀")
    return ELEVATOR_PITCH

def is_valid_ticker(ticker: str) -> bool:
    return ticker.startswith('$') and len(ticker) <= 6 and len(ticker) >= 2 and ticker[1:].isupper()  # Check if it starts with '$', is up to 5 characters long, and is uppercase

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
    token_metrics = update.message.text
    
    if not is_valid_token_metrics(token_metrics):
        await update.message.reply_text("Please enter a valid token metrics format (e.g., '1,000,000,000'). 💔")
        return TOKEN_METRICS  # Stay in the same state to ask for the token metrics again
    
    context.user_data['token_metrics'] = token_metrics
    await update.message.reply_text("Initial Supply at TGE (Token Generation Event) 🔓")
    return INITIAL_SUPPLY

def is_valid_token_metrics(metrics: str) -> bool:
    # Check if the format is a valid number with commas

    parts = metrics.split(',')
    # Check if the last part is a valid number
    if not parts[0].isdigit():
        print("the first part is not a number")
        return False

    # Check if all parts except the last one are valid numbers
    for part in parts[1:]:
        if not part.isdigit() or len(part) != 3:  # Each part must be a digit and exactly 3 digits long
            print("the part is not a number or not 3 digits long")
            return False

    return True  # Valid format

async def handle_initial_supply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    initial_supply = update.message.text
    
    if not is_valid_token_metrics(initial_supply):
        await update.message.reply_text("Please enter a valid initial supply format (e.g., '1,000,000'). 💔")
        return INITIAL_SUPPLY  # Stay in the same state to ask for the initial supply again
    
    context.user_data['initial_supply'] = initial_supply
    await update.message.reply_text("Target FDV (Fully Diluted Valuation) 💰")
    return TARGET_FDV

async def handle_target_fdv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    target_fdv = update.message.text
    
    if not is_valid_token_metrics(target_fdv):
        await update.message.reply_text("Please enter a valid FDV format (e.g., '1,000,000,000'). 💔")
        return TARGET_FDV  # Stay in the same state to ask for the target FDV again
    
    context.user_data['target_fdv'] = target_fdv
    await update.message.reply_text("List each category with its percentage using this format: 'XX% - Category Name'. "
                                      "Don't forget to include the percent for your initial liquidity pool that will be burned! 🔥")
    return TOKEN_DISTRIBUTION

async def handle_token_distribution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    token_distribution = update.message.text
    
    if not is_valid_token_distribution(token_distribution):
        await update.message.reply_text("Please enter a valid vesting schedule format. Ensure the total percentage equals 100%. 💔 Example: 50% - Team\n20% - Advisors\n30% - Liquidity")
        return TOKEN_DISTRIBUTION  # Stay in the same state to ask for the vesting schedule again
    
    context.user_data['token_distribution'] = token_distribution
    await update.message.reply_text("Let's move on to the Vesting Schedule.\n\n"
                                      "For each category, specify:\n"
                                      "• Cliff period (locked period before first unlock) in months\n"
                                      "• Initial unlock percentage (TGE unlock)\n"
                                      "• Vesting duration and details (in months)\n\n"
                                      "Example format:\n"
                                      "Team (20%):\n"
                                      "• 3 month cliff\n"
                                      "• 0% initial unlock\n"
                                      "• 12 months linear vesting\n\n"
                                      "Community (69%):\n"
                                      "• 0 month cliff\n"
                                      "• 10% initial unlock\n"
                                      "• 6 months linear vesting\n\n"
                                      "Please provide vesting details for your categories (copy - paste - complete):\n\n"
                                      f"Based on their previous answer ({context.user_data['token_distribution']}):")
    return VESTING_SCHEDULE

def is_valid_token_distribution(token_distribution: str) -> bool:
    lines = token_distribution.splitlines()
    total_percentage = 0

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        parts = line.split('-')
        if len(parts) != 2:
            return False  # Must be in the format 'XX% - Category Name'
        
        percentage_part = parts[0].strip()
        category_part = parts[1].strip()

        # Check if the percentage part is valid
        if not percentage_part.endswith('%') or not percentage_part[:-1].isdigit():
            return False  # Must be a valid percentage

        # Add to total percentage
        total_percentage += int(percentage_part[:-1])  # Convert to integer and add

    return total_percentage == 100  # Check if total percentage equals 100


async def handle_vesting_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    vesting_schedule = update.message.text
    
    if not is_valid_vesting_schedule(vesting_schedule):
        await update.message.reply_text("Please enter a valid vesting schedule format. Ensure the total percentage equals 100%. 💔")
        return VESTING_SCHEDULE  # Stay in the same state to ask for the vesting schedule again
    
    context.user_data['vesting_schedule'] = vesting_schedule
    await update.message.reply_text("Project Roadmap & Team 🗺️\n\n"
                                      "Please outline your quarterly roadmap for the next 6-12 months. "
                                      "For each quarter, list 2-3 key objectives in bullet points.")
    return ROADMAP

def extract_vesting_schedule(vesting_schedule: str) -> list:
    lines = vesting_schedule.splitlines()
    result = []
    current_category = None

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        # Check if the line is a category
        if ':' in line:
            if current_category:  # If we have a current category, save it before moving to the next
                result.append(current_category)

            parts = line.split(':')
            category_name = parts[0].strip()
            current_category = [category_name, []]  # Initialize the current category with an empty list for details
        else:
            # Process detail lines
            if current_category is not None and line.startswith('•'):
                detail = line[1:].strip()  # Remove the bullet point
                # Extract the number of months from the detail
                if "month cliff" in detail:
                    months = int(detail.split()[0])  # Get the number of months
                    current_category[1].append(months)
                elif "initial unlock" in detail:
                    percentage = int(detail.split()[0].replace('%', ''))  # Get the percentage
                    current_category[1].append(percentage)
                elif "months linear vesting" in detail:
                    months = int(detail.split()[0])  # Get the number of months
                    current_category[1].append(months)

    # Append the last category if it exists
    if current_category:
        result.append(current_category)

    return result

def is_valid_vesting_schedule(vesting_schedule: str) -> bool:
    # lines = vesting_schedule.splitlines()
    # print('lines', lines)
    
    # for line in lines:
    #     line = line.strip()
    #     print('line', line)
    #     if not line:  # Skip empty lines
    #         continue
    #     parts = line.split(':')
    #     print('parts', parts)
    #     if len(parts) != 2:
    #         print(parts)
    #         print('Must be in the format "Category (XX%):"')
    #         return False  # Must be in the format 'Category (XX%):'

    #     category_part = parts[0].strip()
    #     details_part = parts[1].strip()
    #     print('details_part', details_part)
    #     # Check if the details part contains valid vesting details
    #     details_lines = details_part.splitlines()
    #     if len(details_lines) < 3:  # Must have at least 3 details
    #         print('details_lines', details_lines)
    #         print('Must have at least 3 details')
    #         return False

    #     # Check each detail line
    #     for detail in details_lines:
    #         detail = detail.strip()
    #         if not detail:  # Skip empty lines
    #             continue
    #         if not (detail.startswith('•') and len(detail) > 1):
    #             print('Each detail must start with "•"')
    #             return False  # Each detail must start with '•'

    #         # Additional checks for specific details
    #         if "month cliff" not in detail and "TGE unlock" not in detail and "months linear vesting" not in detail:
    #             print('Details must specify cliff, TGE unlock, and vesting duration')
    #             return False  # Must specify cliff, TGE unlock, and vesting duration

    return True

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
                                      "• Why have you chosen to pursue a DEX-only launch? 🤔")
    return DEX_INFO

async def handle_dex_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['dex_info'] = update.message.text
    await update.message.reply_text("Additional Information 📝\n\n"
                                      "9. Launch Strategy & Vision\n"
                                      "• Do you have a powerful quote from a founder or notable personality about your project? "
                                      "Please include their name and title 💭")
    return ADDITIONAL_INFO

async def handle_additional_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['additional_info'] = update.message.text
    await summary(update, context)  # Appel de la fonction summary ici
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
    # Prepare data for plotting
    cumulative_emissions = {}

    print('vesting_schedule_details', vesting_schedule_details)
    print('token_distribution', token_distribution)
    
    for category_with_percentage, details in vesting_schedule_details:
        # Extract the category name without the percentage
        category = category_with_percentage.split('(')[0].strip()

        # Ensure details have the expected length
        if len(details) != 3:
            print(f"Invalid details for category '{category}': {details}")
            continue  # Skip this category if details are not as expected

        cliff_months = details[0]
        initial_unlock = details[1]
        linear_vesting_months = details[2]

        # Calculate the total months for the vesting schedule
        total_months = cliff_months + linear_vesting_months

        # Initialize cumulative emissions for this category
        cumulative_emissions[category] = np.zeros(total_months + 1)

        # Calculate emissions over time
        for month in range(total_months + 1):
            if month < cliff_months:
                cumulative_emissions[category][month] = 0  # No emissions during the cliff period
            elif month == cliff_months:
                cumulative_emissions[category][month] = initial_unlock  # Initial unlock at cliff
            else:
                # Calculate linear vesting emissions
                vesting_amount = (100 - initial_unlock) / linear_vesting_months
                cumulative_emissions[category][month] = initial_unlock + vesting_amount * (month - cliff_months)

    # Debugging: Print cumulative emissions
    print("Cumulative Emissions:", cumulative_emissions)

    # Create a stacked area plot
    plt.figure(figsize=(10, 6))
    for category, emissions in cumulative_emissions.items():
        plt.fill_between(range(len(emissions)), emissions, label=f"{category} ({token_distribution.get(category, 0)}%)")

    plt.title('Cumulative Token Emission Schedule')
    plt.xlabel('Months')
    plt.ylabel('Cumulative Tokens in Circulation (in Millions)')
    plt.xticks(range(len(emissions)))  # Set x-ticks to show each month
    plt.legend(title='Token Categories')
    plt.grid()
    
    # Save the graph as an image
    graph_path = 'cumulative_emission_graph.png'
    plt.savefig(graph_path)
    plt.close()  # Close the plot to free memory

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
        f"Initial Supply at TGE: {context.user_data['initial_supply']} 🔓\n"
        f"Target FDV: {context.user_data['target_fdv']} 💰\n"
        f"Token Distribution: {context.user_data['token_distribution']} 📊\n"
        f"Vesting Schedule: {context.user_data['vesting_schedule']} ⏳\n"
        f"Roadmap: {context.user_data['roadmap']} 🗺️\n"
        f"Team Info: {context.user_data['team_info']} 👥\n"
        f"Essential Links: {context.user_data['essential_links']} 🔗\n"
        f"Additional Info: {context.user_data['additional_info']} 📝\n"
        f"DEX Info: {context.user_data['dex_info']} 📝\n\n"
        "✨ Thank you for submitting your project to BorgPad! ✨"
    )
    
    await update.message.reply_text(recap)

    # Create and send the pie chart
    chart_path = create_pie_chart(context.user_data['token_distribution'])
    with open(chart_path, 'rb') as chart_file:
        await update.message.reply_photo(photo=chart_file)

    # Parse the token distribution
    token_distribution = parse_token_distribution(context.user_data['token_distribution'])
    vesting_schedule_details = extract_vesting_schedule(context.user_data['vesting_schedule'])
    print('vesting_schedule_details', vesting_schedule_details)
    # Create and send the cumulative emission graph
    cumulative_graph_path = create_cumulative_emission_graph(vesting_schedule_details, token_distribution)
    with open(cumulative_graph_path, 'rb') as cumulative_graph_file:
        await update.message.reply_photo(photo=cumulative_graph_file)

    return ConversationHandler.END



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
            INITIAL_SUPPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_initial_supply)],
            TARGET_FDV: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_fdv)],
            TOKEN_DISTRIBUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token_distribution)],
            VESTING_SCHEDULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vesting_schedule)],
            ROADMAP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roadmap)],
            TEAM_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_team_info)],
            ESSENTIAL_LINKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_essential_links)],
            ADDITIONAL_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_additional_info)],
            DEX_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dex_info)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()