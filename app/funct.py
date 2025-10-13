import sqlite3
from functools import wraps
from flask import session, redirect, url_for

DB_NAME = "angajati.db"

# === Conexiunea la baza de date ===
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# === Creeaza Baza de date ===
def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS angajati(
            /*Indentificare personala*/
            cnp TEXT PRIMARY KEY,
            nume TEXT NOT NULL,
            prenume TEXT NOT NULL,
            data_nasterii DATE,
            varsta INTEGER CHECK (varsta >= 18),
            gen TEXT CHECK (gen IN('M', 'F', 'Altul')),
            nationalitate TEXT,
            stare_civila TEXT,
            nr_copii INTEGER DEFAULT 0,

            /*Date de contact*/
            telefon TEXT,
            adresa_email TEXT,
            adresa_domiciliu TEXT NOT NULL,

            /*Educatie si certificari*/
            nivel_educatie TEXT,
            certificari TEXT,

            /*Date contractuale*/
            nr_contract TEXT,
            tip_contract TEXT NOT NULL CHECK(tip_contract IN('determinat', 'nedeterminat', 'internship')),
            functie TEXT NOT NULL,
            pozitie_companie TEXT,
            departament TEXT,
            senioritate TEXT NOT NULL CHECK (senioritate IN('junior', 'mid', 'senior')),
            norma TEXT NOT NULL CHECK (norma IN ('Full-time', 'Part-time')),
            data_angajare DATE,
            data_incetare_contract DATE,

            /*Date financiare*/
            iban TEXT,
            salariu INTEGER NOT NULL CHECK (salariu >= 4050),
            bonusuri REAL DEFAULT 0,

            /*Concedii*/
            concediu_total INTEGER DEFAULT 20,
            concediu_ramas INTEGER DEFAULT 20,
            medicale INTEGER DEFAULT 0,

            /* Status si altele */
            status_angajat TEXT DEFAULT 'Activ' CHECK (status_angajat IN('Activ', 'Inactiv', 'Suspendat')),
            observatii TEXT
            )
    ''')

    conn.commit()
    conn.close()


# === Login req ===
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session or session['username'] != 'admin':
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return wrapper

# === Calculator ===
class Calculator:
    def calculeaza(self, expresie):
        try:
            rezultat = eval(expresie, {"__builtins__": None}, {})
            return rezultat
        except ZeroDivisionError:
            return "Eroare: împărțire la 0"
        except Exception:
            return "Eroare: expresie invalidă"