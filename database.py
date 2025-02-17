import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    
    # Création de la table projects
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            twitter_username TEXT NOT NULL,
            project_name TEXT NOT NULL,
            token_ticker TEXT NOT NULL,
            elevator_pitch TEXT,
            problem_solving TEXT,
            solution TEXT,
            technology TEXT,
            target_market TEXT,
            growth_strategy TEXT,
            competitors TEXT,
            differentiators TEXT,
            token_metrics TEXT,
            initial_supply TEXT,
            target_fdv TEXT,
            token_distribution TEXT,
            vesting_schedule TEXT,
            roadmap TEXT,
            team_info TEXT,
            essential_links TEXT,
            additional_info TEXT,
            dex_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_project_data(data):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO projects (
            twitter_username, project_name, token_ticker, elevator_pitch,
            problem_solving, solution, technology, target_market,
            growth_strategy, competitors, differentiators, token_metrics,
            initial_supply, target_fdv, token_distribution, vesting_schedule,
            roadmap, team_info, essential_links, additional_info, dex_info
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('username'),
        data.get('project_name'),
        data.get('token_ticker'),
        data.get('elevator_pitch'),
        data.get('problem_solving'),
        data.get('solution'),
        data.get('technology'),
        data.get('target_market'),
        data.get('growth_strategy'),
        data.get('competitors'),
        data.get('differentiators'),
        data.get('token_metrics'),
        data.get('initial_supply'),
        data.get('target_fdv'),
        data.get('token_distribution'),
        data.get('vesting_schedule'),
        data.get('roadmap'),
        data.get('team_info'),
        data.get('essential_links'),
        data.get('additional_info'),
        data.get('dex_info')
    ))
    
    conn.commit()
    conn.close()

def get_project(twitter_username):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM projects WHERE twitter_username = ? ORDER BY created_at DESC LIMIT 1', (twitter_username,))
    project = c.fetchone()
    
    conn.close()
    
    if project:
        # Convertir le tuple en dictionnaire
        columns = ['id', 'twitter_username', 'project_name', 'token_ticker', 'elevator_pitch',
                  'problem_solving', 'solution', 'technology', 'target_market',
                  'growth_strategy', 'competitors', 'differentiators', 'token_metrics',
                  'initial_supply', 'target_fdv', 'token_distribution', 'vesting_schedule',
                  'roadmap', 'team_info', 'essential_links', 'additional_info', 'dex_info',
                  'created_at']
        return dict(zip(columns, project))
    return None 