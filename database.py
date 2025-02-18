import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    
    # Création de la table projects avec uniquement les colonnes nécessaires
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            twitter_username TEXT NOT NULL,
            project_name TEXT NOT NULL,
            project_description TEXT,
            project_picture TEXT,
            website_link TEXT,
            community_link TEXT,
            x_link TEXT,
            deploy_chain TEXT,
            sector TEXT,
            tge_date TEXT,
            fdv TEXT,
            token_ticker TEXT NOT NULL,
            token_picture TEXT,
            data_room TEXT,
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
            twitter_username, project_name, project_description,
            project_picture, website_link, community_link,
            x_link, deploy_chain, sector,
            tge_date, fdv, token_ticker,
            token_picture, data_room
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('username'),
        data.get('project_name'),
        data.get('project_description'),
        data.get('project_picture'),
        data.get('website_link'),
        data.get('community_link'),
        data.get('x_link'),
        data.get('deploy_chain'),
        data.get('sector'),
        data.get('tge_date'),
        data.get('fdv'),
        data.get('token_ticker'),
        data.get('token_picture'),
        data.get('data_room')
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
        columns = ['id', 'twitter_username', 'project_name', 'project_description',
                  'project_picture', 'website_link', 'community_link', 'x_link',
                  'deploy_chain', 'sector', 'tge_date', 'fdv', 'token_ticker',
                  'token_picture', 'data_room', 'created_at']
        return dict(zip(columns, project))
    return None 