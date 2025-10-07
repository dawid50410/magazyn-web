
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from database import Database
import users

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = Database()

# --- Auth ---
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users.verify_user(username, password):
            session['username'] = username
            session['role'] = users.get_role(username)
            flash('Zalogowano pomyślnie', 'success')
            return redirect(url_for('drut_page'))
        else:
            flash('Błędne dane logowania', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Wylogowano', 'info')
    return redirect(url_for('login'))

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Brak uprawnień (admin required)', 'danger')
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    return wrapper

# --- Pages ---
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# DRUT page + JSON search
@app.route('/drut', methods=['GET','POST'])
@login_required
def drut_page():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Brak uprawnień do modyfikacji', 'danger')
            return redirect(url_for('drut_page'))
        form = request.form
        values = (
            form.get('stan',''), form.get('srednica_drutu',''), form.get('gatunek_drutu',''),
            form.get('dostawca',''), form.get('ilosc_szpule_kregi',''), form.get('waga',''),
            form.get('suma_kg',''), form.get('partia_materialu_nr',''), form.get('przewidywana_data_dostawy',''),
            form.get('przyjecie_materialu','')
        )
        db.insert('drut', values)
        flash('Dodano wpis DRUT', 'success')
        return redirect(url_for('drut_page'))
    dane = db.fetch_all('drut')
    return render_template('drut.html', dane=dane, role=session.get('role'))

@app.route('/drut/search')
@login_required
def drut_search():
    q = request.args.get('q','').strip()
    if not q:
        rows = db.fetch_all('drut')
    else:
        rows = db.search('drut', q)
    # convert to list of dicts for JSON
    keys = ['id','stan','srednica_drutu','gatunek_drutu','dostawca','ilosc_szpule_kregi',
            'waga','suma_kg','partia_materialu_nr','przewidywana_data_dostawy','przyjecie_materialu']
    data = [dict(zip(keys, row)) for row in rows]
    return jsonify(data)

@app.route('/drut/delete/<int:record_id>', methods=['POST'])
@login_required
@admin_required
def drut_delete(record_id):
    db.delete('drut', record_id)
    flash('Usunięto rekord', 'info')
    return redirect(url_for('drut_page'))

@app.route('/drut/edit/<int:record_id>', methods=['POST'])
@login_required
@admin_required
def drut_edit(record_id):
    form = request.form
    values = (
        form.get('stan',''), form.get('srednica_drutu',''), form.get('gatunek_drutu',''),
        form.get('dostawca',''), form.get('ilosc_szpule_kregi',''), form.get('waga',''),
        form.get('suma_kg',''), form.get('partia_materialu_nr',''), form.get('przewidywana_data_dostawy',''),
        form.get('przyjecie_materialu','')
    )
    db.update('drut', record_id, values)
    flash('Zaktualizowano rekord', 'success')
    return redirect(url_for('drut_page'))

# SPREZYN page + JSON search
@app.route('/sprezyny', methods=['GET','POST'])
@login_required
def sprezyny_page():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Brak uprawnień do modyfikacji', 'danger')
            return redirect(url_for('sprezyny_page'))
        form = request.form
        values = (
            form.get('klient',''), form.get('nazwa_detalu',''), form.get('nr_rysunku',''),
            form.get('ilosc',''), form.get('rodzaj_sprezyny',''), form.get('gatunek_drutu',''),
            form.get('srednica_dz',''), form.get('dlugosc_lo',''), form.get('liczba_zwoi',''),
            form.get('szlifowanie','')
        )
        db.insert('sprezyny', values)
        flash('Dodano wpis SPRĘŻYN', 'success')
        return redirect(url_for('sprezyny_page'))
    dane = db.fetch_all('sprezyny')
    return render_template('sprezyny.html', dane=dane, role=session.get('role'))

@app.route('/sprezyny/search')
@login_required
def sprezyny_search():
    q = request.args.get('q','').strip()
    if not q:
        rows = db.fetch_all('sprezyny')
    else:
        rows = db.search('sprezyny', q)
    keys = ['id','klient','nazwa_detalu','nr_rysunku','ilosc','rodzaj_sprezyny','gatunek_drutu','srednica_dz','dlugosc_lo','liczba_zwoi','szlifowanie']
    data = [dict(zip(keys, row)) for row in rows]
    return jsonify(data)

@app.route('/sprezyny/delete/<int:record_id>', methods=['POST'])
@login_required
@admin_required
def sprezyny_delete(record_id):
    db.delete('sprezyny', record_id)
    flash('Usunięto rekord', 'info')
    return redirect(url_for('sprezyny_page'))

@app.route('/sprezyny/edit/<int:record_id>', methods=['POST'])
@login_required
@admin_required
def sprezyny_edit(record_id):
    form = request.form
    values = (
        form.get('klient',''), form.get('nazwa_detalu',''), form.get('nr_rysunku',''),
        form.get('ilosc',''), form.get('rodzaj_sprezyny',''), form.get('gatunek_drutu',''),
        form.get('srednica_dz',''), form.get('dlugosc_lo',''), form.get('liczba_zwoi',''),
        form.get('szlifowanie','')
    )
    db.update('sprezyny', record_id, values)
    flash('Zaktualizowano rekord', 'success')
    return redirect(url_for('sprezyny_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
