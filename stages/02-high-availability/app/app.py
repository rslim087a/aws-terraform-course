#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify
import sqlite3
import os
from datetime import datetime
import requests
import json

app = Flask(__name__)
DB_PATH = '/var/app/guestbook.db'

def get_container_metadata():
    """Fetch ECS container metadata"""
    try:
        metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI_V4')
        if metadata_uri:
            task_response = requests.get(f"{metadata_uri}/task", timeout=1)
            task_data = task_response.json()
            task_arn = task_data.get('TaskARN', 'unknown')
            task_id = task_arn.split('/')[-1] if task_arn != 'unknown' else 'unknown'
            az = task_data.get('AvailabilityZone', 'unknown')
            return task_id, az
    except:
        pass
    return 'unknown', 'unknown'

def init_db():
    """Initialize the SQLite database"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_entries():
    """Get all guestbook entries"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, message, timestamp FROM entries ORDER BY id DESC LIMIT 10')
    entries = cursor.fetchall()
    conn.close()
    return entries

@app.route('/')
def home():
    """Main page showing guestbook"""
    task_id, az = get_container_metadata()
    entries = get_entries()
    return render_template(
        'index.html',
        task_id=task_id,
        az=az,
        entries=entries
    )

@app.route('/sign', methods=['POST'])
def sign():
    """Add a new guestbook entry"""
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        return jsonify({'status': 'error', 'message': 'Name and message are required'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Entry added!'})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
