#  Gestionare Angajați

Aplicația **Gestionare Angajați** este un proiect complet dezvoltat în **Python** folosind **Flask** și **SQLite3**, destinat administrării datelor despre angajați într-o firmă.  
Aceasta oferă funcționalități precum login securizat, adăugare/modificare/ștergere angajați, calcul salarii, generare fluturași PDF și gestionarea statusului angajaților activi/inactivi.

---

##  Funcționalități principale

**Autentificare (Login)** — acces securizat doar pentru administrator.  
**Adăugare, modificare și ștergere angajați** — interfață intuitivă pentru gestionarea completă a personalului.  
**Calcul salariu** — calcul automat bazat pe datele introduse.  
**Generare fluturaș salariu în format PDF** — salvare și descărcare automată.  
**Filtrare angajați activi/inactivi** — vizualizare rapidă a personalului activ.  
**Setare automată a statusului „Inactiv”** la încetarea contractului.  
**Resetare concediu rămas** la trecerea unui angajat în „inactiv”.  

---

##  Tehnologii și librării utilizate

Aplicația este dezvoltată exclusiv în Python, folosind următoarele librării și module:

| Categoria | Pachet / Modul | Descriere |
|------------|----------------|-----------|
| **Framework Web** | `Flask` | Gestionează rutele, sesiunile și template-urile HTML |
| **Bază de date** | `sqlite3` | Baza de date locală pentru angajați |
| **Date și timp** | `datetime`, `timedelta` | Manipularea datelor contractuale |
| **Export PDF** | `reportlab` | Generarea fluturașilor de salariu PDF |
| **Procesare fișiere** | `io.BytesIO` | Crearea fișierelor PDF în memorie |
| **Autentificare** | `functools.wraps`, `session` | Decorator pentru rute protejate și management login |
| **Analiză date (extensibil)** | `pandas` | Prelucrare și export de tabele, rapoarte sau statistici |
| **Diverse** | `flash`, `redirect`, `render_template`, `url_for`, `make_response` | Funcții utile Flask pentru UX și control rutare |

```
gestionare-angajati/
├── app/
│ ├── __init__.py
│ ├── funct.py
│ ├── routes.py
├── templates/ — folder cu fișierele HTML (interfața web)
│ ├── adauga.html
│ ├── afisare.html
│ ├── calcul_salar.html
│ ├── fluturas.html
│ ├── index.html
│ ├── login.html
│ ├── modifica.html
│ └── salarizare.html
├── amain.py
├── angajati.db
├── angajati.xlsx, angajati_export.xlsx 
└── README.md 
```


##  Instalare și rulare locală

1. **Clonează proiectul**
   ```bash
   git clone https://github.com/<numele-tău-utilizator>/gestionare-angajati.git
   cd gestionare-angajati

BASH

python -m venv venv

source venv/bin/activate     # Linux / Mac

venv\Scripts\activate        # Windows

pip install flask pandas reportlab

python main.py

Acceseaza in browser

http://127.0.0.1:5000/

Autentifică-te cu contul de administrator (admin / parola123)


Autor - Alexandru Cioara 2025
