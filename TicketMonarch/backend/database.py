import sqlite3
import csv
import os
from datetime import datetime

# Get base directory and data directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'checkouts.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def init_database():
    """Initialize the database and create the checkouts table"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            card_number TEXT,
            card_expiry TEXT,
            card_cvv TEXT,
            billing_address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_order(order_data):
    """Save submitted form data to the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO checkouts (full_name, email, card_number, card_expiry, card_cvv, 
                              billing_address, city, state, zip_code, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_data.get('full_name', ''),
        order_data.get('email', ''),
        order_data.get('card_number', ''),
        order_data.get('card_expiry', ''),
        order_data.get('card_cvv', ''),
        order_data.get('billing_address', ''),
        order_data.get('city', ''),
        order_data.get('state', ''),
        order_data.get('zip_code', ''),
        datetime.now().isoformat()
    ))
    
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return order_id

def export_to_csv():
    """Export all checkout data to a CSV file in the data/ folder"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM checkouts')
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    conn.close()
    
    csv_path = os.path.join(DATA_DIR, 'checkouts.csv')
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)
    
    return csv_path

