# LifeDays — навчальний CI/CD

Python 3.12, Flask, Gunicorn, Nginx, Jenkins. Інструкції налаштування чотирьох ВМ наведено в супровідному посібнику.

Локальний запуск:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m flask --app app run --host 0.0.0.0
```

Jenkins: label `linux-python`, SSH credential `deploy-ssh`, GitHub SSH credential configured in SCM. First build manually; then polling every two minutes. Use only trusted commits on main. Deployment: 192.168.56.104. The server needs access to PyPI. No real birth dates in tests. Dependency ranges are educational, not a reproducible production lockfile.
