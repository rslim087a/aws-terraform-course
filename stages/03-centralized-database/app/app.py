#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify
import os
from datetime import datetime
import subprocess
import pymysql

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'guestbook')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_container_metadata():
    """Fetch ECS container metadata"""
    try:
        import requests
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, message, timestamp FROM entries ORDER BY id DESC LIMIT 10')
    entries = cursor.fetchall()
    conn.close()
    return [(e['name'], e['message'], e['timestamp']) for e in entries]

@app.route('/')
def home():
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
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        return jsonify({'status': 'error', 'message': 'Name and message are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (name, message) VALUES (%s, %s)', (name, message))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Entry added!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
