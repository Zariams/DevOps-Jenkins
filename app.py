from datetime import date
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from calculator import calculate_days

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4096
VERSION = Path(__file__).with_name('VERSION').read_text().strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    today = date.today()
    result, error = None, None
    birth = ''
    if request.method == 'POST':
        birth = request.form.get('birth_date', '')
        try:
            parsed = date.fromisoformat(birth)
            if parsed.isoformat() != birth:
                raise ValueError('format')
            result = calculate_days(parsed, today)
        except ValueError:
            error = 'Введіть коректну дату, не пізнішу за сьогодні.'
    return render_template('index.html', result=result, error=error,
                           birth=birth, today=today.isoformat(), version=VERSION), (400 if error else 200)

@app.get('/health')
def health():
    return jsonify(status='ok', version=VERSION)

@app.after_request
def privacy(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
