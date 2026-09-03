from flask import Flask, render_template, request, redirect, url_for, session, send_file, Response
import sqlite3, os, io
from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)
app.secret_key = "almahyra_rahasia_2026"
DB = 'kas.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kas
                 (id INTEGER PRIMARY KEY, tanggal TEXT, keterangan TEXT, masuk REAL, keluar REAL)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['pass'] == 'almahyra123':
            session['login'] = True
            return redirect(url_for('kas'))
        return "Login gagal"
    return render_template('login.html')

@app.route('/kas', methods=['GET', 'POST'])
def kas():
    if 'login' not in session: return redirect(url_for('login'))
    init_db()
    if request.method == 'POST':
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO kas (tanggal,keterangan,masuk,keluar) VALUES (?,?,?,?)",
                  (request.form['tanggal'], request.form['ket'], request.form['masuk'], request.form['keluar']))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB)
    data = conn.cursor().execute("SELECT * FROM kas ORDER BY tanggal DESC").fetchall()
    conn.close()
    return render_template('kas.html', data=data)

@app.route('/pdf')
def pdf():
    # Kode bikin PDF laporan
    return "Fitur PDF"

if __name__ == '__main__':
    app.run(debug=True)
