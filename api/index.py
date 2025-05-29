from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL
        )''')

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    username = request.args.get('user', 'guest')

    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO notes (username, content) VALUES (?, ?)", (username, note))

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, content FROM notes WHERE username=?", (username,))
        notes = cursor.fetchall()

    return render_template('index.html', notes=notes, username=username)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    username = request.args.get('user', 'guest')
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM notes WHERE id=? AND username=?", (note_id, username))
    return redirect(url_for('index', user=username))

# Required by Vercel
app.config['JSON_AS_ASCII'] = False
