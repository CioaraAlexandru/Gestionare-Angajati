from flask import Flask, flash, render_template, request, send_file, redirect,make_response, session, url_for
import sqlite3
from functools import wraps
import pandas as pd
from datetime import datetime, date, timedelta

from joblib import expires_after
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


from matplotlib.backend_bases import cursors

# DB_NAME = "angajati.db"
#
# # === Conexiunea la baza de date ===
# def get_connection():
#     conn = sqlite3.connect(DB_NAME)
#     return conn
#
#
# def init_db():
#     conn = get_connection()
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS angajati(
#             /*Indentificare personala*/
#             cnp TEXT PRIMARY KEY,
#             nume TEXT NOT NULL,
#             prenume TEXT NOT NULL,
#             data_nasterii DATE,
#             varsta INTEGER CHECK (varsta >= 18),
#             gen TEXT CHECK (gen IN('M', 'F', 'Altul')),
#             nationalitate TEXT,
#             stare_civila TEXT,
#             nr_copii INTEGER DEFAULT 0,
#
#             /*Date de contact*/
#             telefon TEXT,
#             adresa_email TEXT,
#             adresa_domiciliu TEXT NOT NULL,
#
#             /*Educatie si certificari*/
#             nivel_educatie TEXT,
#             certificari TEXT,
#
#             /*Date contractuale*/
#             nr_contract TEXT,
#             tip_contract TEXT NOT NULL CHECK(tip_contract IN('determinat', 'nedeterminat', 'internship')),
#             functie TEXT NOT NULL,
#             pozitie_companie TEXT,
#             departament TEXT,
#             senioritate TEXT NOT NULL CHECK (senioritate IN('junior', 'mid', 'senior')),
#             norma TEXT NOT NULL CHECK (norma IN ('Full-time', 'Part-time')),
#             data_angajare DATE,
#             data_incetare_contract DATE,
#
#             /*Date financiare*/
#             iban TEXT,
#             salariu INTEGER NOT NULL CHECK (salariu >= 4050),
#             bonusuri REAL DEFAULT 0,
#
#             /*Concedii*/
#             concediu_total INTEGER DEFAULT 20,
#             concediu_ramas INTEGER DEFAULT 20,
#             medicale INTEGER DEFAULT 0,
#
#             /* Status si altele */
#             status_angajat TEXT DEFAULT 'Activ' CHECK (status_angajat IN('Activ', 'Inactiv', 'Suspendat')),
#             observatii TEXT
#             )
#     ''')
#
#     conn.commit()
#     conn.close()
#
#
# app = Flask(__name__)
# app.secret_key = 'thorecainedestept'
#
# init_db()
#
# # ======= Login req ========
# def login_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if 'username' not in session or session['username'] != 'admin':
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return wrapper

# # Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form.get('username', '').strip()
#         password = request.form.get('password', '').strip()
#
#         # credențiale fixe pentru proiect (schimbă în producție!)
#         if username == 'admin' and password == 'parola123':
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             error = "Utilizator sau parolă incorectă."
#
#     return render_template('login.html', error=error, current_year=datetime.now().year)
#
#
# # Logout
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect('/login')
#
#
# # Index
# @app.route('/')
# @login_required
# def index():
#     conn = get_connection()
#     angajati = conn.execute('SELECT cnp, nume, prenume, varsta, salariu, departament, senioritate FROM angajati').fetchall()
#     return render_template('index.html', angajati=angajati)
#
#
#
#
# # === Adaugare angajat in DB ===
# @app.route('/adauga', methods=['GET', 'POST'])
# @login_required
# def adauga_angajat():
#     if request.method == 'POST':
#         try:
#             #Date personale
#             cnp = request.form['cnp']
#             nume = request.form['nume']
#             prenume = request.form['prenume']
#
#             data_nasterii_str = request.form.get('data_nasterii')
#             data_nasterii = datetime.strptime(data_nasterii_str, "%Y-%m-%d").date() if data_nasterii_str else None
#
#             today = date.today()
#             if data_nasterii:
#                 varsta = today.year - data_nasterii.year - (
#                             (today.month, today.day) < (data_nasterii.month, data_nasterii.day))
#             else:
#                 varsta = None
#
#             gen = request.form['gen']
#             nationalitate = request.form['nationalitate']
#             stare_civila = request.form.get('stare_civila')
#             nr_copii = request.form.get('nr_copii', 0)
#
#             #Daate de contact
#             telefon = request.form.get('telefon')
#             adresa_email = request.form.get('adresa_email')
#             adresa_domiciliu = request.form['adresa_domiciliu']
#
#             #Educație și certificări
#             nivel_educatie = request.form.get('nivel_educatie')
#             certificari = request.form.get('certificari')
#
#             #Contract
#             nr_contract = request.form.get('nr_contract')
#             tip_contract = request.form['tip_contract']
#             functie = request.form['functie']
#             pozitie_companie = request.form.get('pozitie_companie')
#             departament = request.form['departament']
#             senioritate = request.form['senioritate']
#             norma = request.form['norma']
#             data_angajare = request.form.get('data_angajare')
#             data_incetare_contract = request.form.get('data_incetare_contract')
#
#             #Financiar
#             iban = request.form.get('iban')
#             salariu = int(request.form['salariu'])
#             bonusuri = request.form.get('bonusuri')
#
#             #Concedii
#             concediu_total = int(request.form.get('concediu_total') or 20)
#             concediu_ramas = concediu_total
#             medicale = 0
#
#             #Status & altele
#             status_angajat = request.form.get('status_angajat', 'Activ')
#             observatii = request.form.get('observatii')
#
#
#             if len(cnp) != 13 or not cnp.isdigit():
#                 return "CNP invalid. Trebuie să aibă exact 13 cifre.", 400
#             if varsta < 18:
#                 return "Vârsta trebuie să fie minim 18 ani.", 400
#             if salariu < 4050:
#                 return "Salariul trebuie să fie cel puțin 4050 lei (minim pe economie).", 400
#             if senioritate not in ['junior', 'mid', 'senior']:
#                 return "Senioritate invalidă.", 400
#             if tip_contract not in ['determinat', 'nedeterminat', 'intership']:
#                 return "Tip contract invalid.", 400
#             if norma not in ['Full-time', 'Part-time']:
#                 return "Norma invalidă.", 400
#
#
#             conn = sqlite3.connect('angajati.db')
#             cursor = conn.cursor()
#
#
#             cursor.execute("SELECT 1 FROM angajati WHERE cnp = ?", (cnp,))
#             if cursor.fetchone():
#                 conn.close()
#                 return "Un angajat cu acest CNP există deja.", 400
#
#             cursor.execute("""
#                 INSERT INTO angajati (
#                     cnp, nume, prenume, data_nasterii, varsta, gen, nationalitate, stare_civila, nr_copii,
#                     telefon, adresa_email, adresa_domiciliu,
#                     nivel_educatie, certificari,
#                     nr_contract, tip_contract, functie, pozitie_companie, departament, senioritate, norma, data_angajare, data_incetare_contract,
#                     iban, salariu, bonusuri,
#                     concediu_total, concediu_ramas, medicale,
#                     status_angajat, observatii
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 cnp, nume, prenume, data_nasterii, varsta, gen, nationalitate, stare_civila, nr_copii,
#                 telefon, adresa_email, adresa_domiciliu,
#                 nivel_educatie, certificari,
#                 nr_contract, tip_contract, functie, pozitie_companie, departament, senioritate, norma, data_angajare, data_incetare_contract,
#                 iban, salariu, bonusuri,
#                 concediu_total, concediu_ramas, medicale,
#                 status_angajat, observatii
#             ))
#
#             conn.commit()
#             conn.close()
#             return redirect('/afisare')
#
#         except Exception as e:
#             return f"Eroare la introducere: {str(e)}", 500
#
#     else:
#         return render_template('adauga.html')
#
#
#
# # === Afisare angajati si filtrare ===
# @app.route('/afisare', methods=['GET', 'POST'])
# @login_required
# def afisare_angajati():
#     with sqlite3.connect('angajati.db') as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#
#         cursor.execute("SELECT DISTINCT departament FROM angajati")
#         departamente = [row[0] for row in cursor.fetchall()]
#
#         cursor.execute("SELECT DISTINCT functie FROM angajati")
#         functii = [row[0] for row in cursor.fetchall()]
#
#         senioritati = ["junior", "mid", "senior"]
#         norme = ["Full-time", "Part-time"]
#         statusuri = ["Activ", "Inactiv", "Suspendat"]
#
#         query = "SELECT * FROM angajati WHERE 1=1"
#         params = []
#
#         departament_selectat = "Toate"
#         senioritate_selectata = "Toate"
#         functie_selectata = "Toate"
#         norma_selectata = "Toate"
#         status_selectat = "Toate"
#         salariu_min = ""
#         salariu_max = ""
#         nume_cautat = ""
#
#         if request.method == 'POST':
#             departament_selectat = request.form.get("departament", "Toate")
#             senioritate_selectata = request.form.get("senioritate", "Toate")
#             functie_selectata = request.form.get("functie", "Toate")
#             norma_selectata = request.form.get("norma", "Toate")
#             status_selectat = request.form.get("status", "Toate")
#             salariu_min = request.form.get("salariu_min", "")
#             salariu_max = request.form.get("salariu_max", "")
#             nume_cautat = request.form.get("nume_cautat", "")
#
#             if departament_selectat != "Toate":
#                 query += " AND departament = ?"
#                 params.append(departament_selectat)
#
#             if senioritate_selectata != "Toate":
#                 query += " AND senioritate = ?"
#                 params.append(senioritate_selectata)
#
#             if functie_selectata != "Toate":
#                 query += " AND functie = ?"
#                 params.append(functie_selectata)
#
#             if norma_selectata != "Toate":
#                 query += " AND norma = ?"
#                 params.append(norma_selectata)
#
#             if status_selectat != "Toate":
#                 query += " AND status_angajat = ?"
#                 params.append(status_selectat)
#
#             if salariu_min:
#                 query += " AND salariu >= ?"
#                 params.append(salariu_min)
#
#             if salariu_max:
#                 query += " AND salariu <= ?"
#                 params.append(salariu_max)
#
#             if nume_cautat:
#                 query += " AND (nume LIKE ? OR prenume LIKE ?)"
#                 params.append(f"%{nume_cautat}")
#                 params.append(f"%{nume_cautat}")
#
#         cursor.execute(query, params)
#         angajati = cursor.fetchall()
#
#     return render_template(
#         'afisare.html',
#         angajati=angajati,
#         departamente=departamente,
#         functii=functii,
#         senioritati=senioritati,
#         norme=norme,
#         statusuri=statusuri,
#         departament_selectat=departament_selectat,
#         senioritate_selectata=senioritate_selectata,
#         functie_selectata=functie_selectata,
#         norma_selectata=norma_selectata,
#         status_selectat=status_selectat,
#         salariu_min=salariu_min,
#         salariu_max=salariu_max,
#         nume_cautat=nume_cautat
#     )
#
#
#
#
# # === Sterge angajat ===
# @app.route('/sterge/<cnp>', methods=['GET', 'POST'])
# @login_required
# def sterge_angajat(cnp):
#     conn = sqlite3.connect('angajati.db')
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM angajati WHERE cnp = ?', (cnp,))
#     conn.commit()
#     conn.close()
#     return redirect('/afisare')
#
#
# # === Modificare angajat ===
# @app.route('/modifica/<cnp>', methods=['GET', 'POST'])
# @login_required
# def formular_modificare(cnp):
#     conn = sqlite3.connect('angajati.db')
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT * FROM angajati WHERE cnp = ?", (cnp,))
#     angajat = cursor.fetchone()
#
#     if not angajat:
#         conn.close()
#         return "Angajatul nu a fost găsit", 404
#
#     if request.method == 'POST':
#         nume = request.form['nume']
#         prenume = request.form['prenume']
#         data_nasterii_str = request.form.get('data_nasterii')
#         telefon = request.form['telefon']
#         adresa_email = request.form['adresa_email']
#         adresa_domiciliu = request.form['adresa_domiciliu']
#         nivel_educatie = request.form['nivel_educatie']
#         functie = request.form['functie']
#         departament = request.form['departament']
#         senioritate = request.form['senioritate']
#         norma = request.form['norma']
#         iban = request.form['iban']
#         salariu = int(request.form['salariu'])
#         data_angajare = request.form['data_angajare']
#         data_incetare_contract = request.form['data_incetare_contract']
#         concediu_total = request.form['concediu_total']
#         status_angajat = request.form['status_angajat']
#
#         varsta = None
#
#         if data_nasterii_str:
#             from datetime import datetime, date
#             dob = datetime.strptime(data_nasterii_str, "%Y-%m-%d").date()
#             azi = date.today()
#             varsta = azi.year - dob.year - ((azi.month, azi.day) < (dob.month, dob.day))
#
#         status_angajat = "Activ"
#         if data_incetare_contract:
#             status_angajat = "Inactiv"
#             concediu_ramas = 0
#
#         if salariu < 4050:
#             conn.close()
#             return "Salariul trebuie să fie minim pe economie (4050 lei)", 400
#         if senioritate not in ['junior', 'mid', 'senior']:
#             conn.close()
#             return "Senioritate invalidă.", 400
#
#         cursor.execute("""
#             UPDATE angajati
#             SET nume = ?, prenume = ?, data_nasterii = ?, varsta = ?, telefon = ?,
#                 adresa_email = ?, adresa_domiciliu = ?, nivel_educatie = ?, functie = ?,
#                 departament = ?, senioritate = ?, norma = ?, iban = ?, salariu = ?,
#                 data_angajare = ?, data_incetare_contract = ?, status_angajat = ?
#             WHERE cnp = ?
#         """, (nume, prenume, data_nasterii_str, varsta, telefon, adresa_email, adresa_domiciliu,
#               nivel_educatie, functie, departament, senioritate, norma, iban, salariu,
#               data_angajare, data_incetare_contract, status_angajat, cnp))
#
#         conn.commit()
#         conn.close()
#         return redirect('/afisare')
#
#     conn.close()
#     return render_template('modifica.html', angajat=angajat)
#
#
# # === CALCUL SALAR ===
# @app.route('/calcul_salar/<cnp>', methods=['GET', 'POST'])
# @login_required
# def calcul_salar(cnp):
#     import calendar
#
#     # preluare angajat
#     with sqlite3.connect('angajati.db', timeout=10) as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM angajati WHERE cnp = ?", (cnp,))
#         angajat = cursor.fetchone()
#
#     if not angajat:
#         return "Angajatul nu a fost gasit", 404
#
#     if request.method == 'POST':
#         an = int(request.form.get('an', '2025'))
#         luna = int(request.form.get('luna', datetime.now().strftime('%m')))
#         zile_lucrate = int(request.form.get('zile_lucrate') or 0)
#         zile_co = int(request.form.get('zile_co') or 0)
#         zile_medicale = int(request.form.get('zile_medicale') or 0)
#
#         salariu_baza = angajat['salariu']
#
#         # calculează zile lucrătoare reale din lună
#         zile_in_luna = calendar.monthrange(an, luna)[1]
#         # excludem sâmbete și duminici
#         zile_lucratoare = sum(
#             1 for zi in range(1, zile_in_luna + 1)
#             if date(an, luna, zi).weekday() < 5
#         )
#
#         salariu_zi = salariu_baza / max(zile_lucratoare, 21)
#
#         plata_lucrate = round(zile_lucrate * salariu_zi, 2)
#         plata_co = round(zile_co * salariu_zi, 2)
#         plata_medicale = round(zile_medicale * salariu_zi * 0.75, 2)
#
#         salariu_total = round(plata_lucrate + plata_co + plata_medicale, 2)
#
#         # calcule CAS, CASS, impozit
#         CAS = round(salariu_total * 0.10, 2)
#         CASS = round(salariu_total * 0.25, 2)
#         impozit = round((salariu_total - CAS - CASS) * 0.10, 2)
#         salariu_net = round(salariu_total - CAS - CASS - impozit, 2)
#
#         # actualizează concediu_ramas
#         if zile_co > 0:
#             with sqlite3.connect('angajati.db', timeout=10) as conn:
#                 cursor = conn.cursor()
#                 nou_concediu = max(0, angajat['concediu_ramas'] - zile_co)
#                 cursor.execute(
#                     "UPDATE angajati SET concediu_ramas = ? WHERE cnp = ?",
#                     (nou_concediu, cnp)
#                 )
#                 conn.commit()
#                 angajat = dict(angajat)
#                 angajat['concediu_ramas'] = nou_concediu
#
#         # trimitem date detaliate către fluturaș
#         return render_template(
#             'fluturas.html',
#             angajat=angajat,
#             an=an,
#             luna=luna,
#             zile_lucrate=zile_lucrate,
#             zile_co=zile_co,
#             zile_medicale=zile_medicale,
#             ore_lucrate=zile_lucrate * 8,
#             salariu_baza=salariu_baza,
#             salariu_total=salariu_total,
#             plata_lucrate=plata_lucrate,
#             plata_co=plata_co,
#             plata_medicale=plata_medicale,
#             CAS=CAS,
#             CASS=CASS,
#             impozit=impozit,
#             salariu_net=salariu_net
#         )
#
#     return render_template('calcul_salar.html', angajat=angajat)
#
#
#
#
#
# # === Salarizare ==
# @app.route('/salarizare')
# @login_required
# def salarizare():
#     conn = sqlite3.connect("angajati.db")
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM angajati WHERE status_angajat = 'Activ'")
#     angajati = cursor.fetchall()
#     conn.close()
#
#     return render_template("salarizare.html", angajati=angajati)
#
#
#
# # === Generare fluturas angajat ===
# @app.route('/fluturas_salar/<cnp>/<an>/<luna>')
# @login_required
# def fluturas_salar(cnp, an, luna):
#     conn = sqlite3.connect("angajati.db")
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#
#     # Datele angajatului
#     cursor.execute("SELECT * FROM angajati WHERE cnp = ?", (cnp,))
#     angajat = cursor.fetchone()
#
#     # Datele de salarizare din tabelul pontaj (sau echivalent)
#     cursor.execute("""
#         SELECT * FROM pontaj
#         WHERE cnp = ? AND an = ? AND luna = ?
#     """, (cnp, an, luna))
#     pontaj = cursor.fetchone()
#     conn.close()
#
#     if not angajat or not pontaj:
#         return "Nu există date pentru acest angajat/lună", 404
#
#     # Extragem datele
#     nume = angajat["nume"]
#     prenume = angajat["prenume"]
#     departament = angajat["departament"]
#     salariu_baza = angajat["salariu"]
#     concediu_total = angajat["concediu_total"]
#     concediu_ramas = angajat["concediu_ramas"]
#
#     zile_lucrate = pontaj["zile_lucrate"]
#     concediu = pontaj["zile_concediu"]
#     medical = pontaj["zile_medical"]
#     ore_lucrate = zile_lucrate * 8
#
#     # Calcul salariu brut proporțional
#     salariu_brut = round(salariu_baza * (zile_lucrate / 21), 2)
#
#     # Scăderi sociale
#     CAS = round(salariu_brut * 0.25, 2)
#     CASS = round(salariu_brut * 0.10, 2)
#     impozit = round((salariu_brut - CAS - CASS) * 0.10, 2)
#     salariu_net = round(salariu_brut - CAS - CASS - impozit, 2)
#
#     return render_template(
#         "fluturas.html",
#         nume=nume,
#         prenume=prenume,
#         departament=departament,
#         salariu_baza=salariu_baza,
#         concediu_total=concediu_total,
#         concediu_ramas=concediu_ramas,
#         zile_lucrate=zile_lucrate,
#         ore_lucrate=ore_lucrate,
#         concediu=concediu,
#         medical=medical,
#         an=an,
#         luna=luna,
#         salariu_brut=salariu_brut,
#         CAS=CAS,
#         CASS=CASS,
#         impozit=impozit,
#         salariu_net=salariu_net
#     )
#
# @app.route('/fluturas_pdf/<cnp>/<an>/<luna>')
# @login_required
# def fluturas_pdf(cnp, an, luna):
#     with sqlite3.connect("angajati.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM angajati WHERE cnp = ?", (cnp,))
#         angajat = cursor.fetchone()
#
#     if not angajat:
#         return "Angajatul nu a fost găsit", 404
#
#     # Simpplu: luam salariu brut
#     salariu_brut = angajat["salariu"]
#     CAS = round(salariu_brut * 0.10, 2)
#     CASS = round(salariu_brut * 0.25, 2)
#     impozit = round((salariu_brut - CAS - CASS) * 0.10, 2)
#     salariu_net = round(salariu_brut - CAS - CASS - impozit, 2)
#
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4
#
#     y = height - 50
#     p.setFont("Helvetica-Bold", 14)
#     p.drawString(200, y, "Fluturaș de salariu")
#     y -= 40
#
#     p.setFont("Helvetica", 12)
#     p.drawString(50, y, f"Angajat: {angajat['nume']} {angajat['prenume']}")
#     y -= 20
#     p.drawString(50, y, f"CNP: {angajat['cnp']}")
#     y -= 20
#     p.drawString(50, y, f"An: {an}  Luna: {luna}")
#     y -= 40
#
#     p.drawString(50, y, f"Salariu brut: {salariu_brut} lei")
#     y -= 20
#     p.drawString(50, y, f"CAS (10%): {CAS} lei")
#     y -= 20
#     p.drawString(50, y, f"CASS (25%): {CASS} lei")
#     y -= 20
#     p.drawString(50, y, f"Impozit: {impozit} lei")
#     y -= 20
#     p.drawString(50, y, f"Salariu net: {salariu_net} lei")
#
#     p.showPage()
#     p.save()
#
#     pdf = buffer.getvalue()
#     buffer.close()
#
#     response = make_response(pdf)
#     response.headers["Content-Type"] = "application/pdf"
#     response.headers["Content-Disposition"] = f"attachment; filename=fluturas_{angajat['nume']}_{an}_{luna}.pdf"
#     return response
#
# # === Exporta fisierul cu toti angajati in format excel ===
# @app.route('/export_excel')
# @login_required
# def export_excel():
#     with sqlite3.connect('angajati.db') as conn:
#         df = pd.read_sql_query(
#             """SELECT cnp, nume, prenume, varsta, data_nasterii, gen, nationalitate,
#                stare_civila, nr_copii, telefon, adresa_email, adresa_domiciliu, nivel_educatie,
#                certificari, nr_contract, tip_contract, functie, pozitie_companie,
#                departament, senioritate, norma, data_angajare, data_incetare_contract,
#                iban, salariu, bonusuri, concediu_total, concediu_ramas, medicale,
#                status_angajat, observatii
#                FROM angajati""",
#             conn
#         )
#
#     file_path = "angajati_export.xlsx"
#     df.to_excel(file_path, index=False, engine="openpyxl")
#
#     return send_file(
#         file_path,
#         as_attachment=True,
#         download_name="angajati.xlsx",
#         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

# # === Calculator ===
# class Calculator:
#     def calculeaza(self, expresie):
#         try:
#             rezultat = eval(expresie, {"__builtins__": None}, {})
#             return rezultat
#         except ZeroDivisionError:
#             return "Eroare: împărțire la 0"
#         except Exception:
#             return "Eroare: expresie invalidă"

# @app.route("/", methods=["GET", "POST"])
# def calculator():
#     rezultat = ""
#     if request.method == "POST":
#         expresie = request.form["expresie"]
#         calc = Calculator()
#         rezultat = calc.calculeaza(expresie)
#     return render_template("index.html", rezultat=rezultat)
#
# # =======================================
#
# if __name__ == '__main__':
#     app.run(debug=True)

