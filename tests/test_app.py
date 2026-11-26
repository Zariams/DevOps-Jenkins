from datetime import date
from app import app

def test_home():
    assert app.test_client().get('/').status_code == 200

def test_today():
    r=app.test_client().post('/',data={'birth_date':date.today().isoformat()})
    assert r.status_code==200 and '0 днів' in r.get_data(as_text=True)

def test_invalid():
    for value in ('','2023-02-29','9999-01-01','bad'):
        assert app.test_client().post('/',data={'birth_date':value}).status_code==400

def test_health():
    r=app.test_client().get('/health')
    assert r.json['status']=='ok' and r.headers['Cache-Control']=='no-store'
