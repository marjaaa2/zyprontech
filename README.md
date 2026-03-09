# Tech Shop Django Starter

Un starter simplu pentru un magazin tech făcut în Django.

## 1. Creează și activează mediul virtual
### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Instalează dependențele
```bash
pip install -r requirements.txt
```

## 3. Rulează migrațiile
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Creează admin
```bash
python manage.py createsuperuser
```

## 5. Pornește site-ul
```bash
python manage.py runserver
```

## 6. Deschide în browser
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Ce poți face
- adaugi produse din admin
- vezi lista produselor pe site
- intri pe pagina fiecărui produs
- modifici stilul din `static/css/style.css`
