from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    message = request.json.get('message')
    timestamp = datetime.now().strftime('%Y.%m.%d %H:%M')

    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute('INSERT INTO entries (message, timestamp) VALUES (?, ?)', (message, timestamp))
    conn.commit()
    entry_id = c.lastrowid
    conn.close()

    return jsonify(success=True, entry={'id': entry_id, 'message': message, 'timestamp': timestamp})

@app.route('/entries', methods=['GET'])
def entries():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute('SELECT message, timestamp FROM entries ORDER BY id DESC')
    entries = [{'message': row[0], 'timestamp': row[1]} for row in c.fetchall()]
    conn.close()

    return jsonify(entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
