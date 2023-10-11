# API to handle everything related to the database, queries, updates and new entries

# HOW TO RUN:

```cd github-app-database-service```

# Create Virtual Env (if not created)

```python -m venv venv```

# Activate Virtual Env

```venv\Scripts\activate```

# Install dependencies

```pip install -r requirements.txt```

# Run migrations

```
python load_env.py
cd src
flask db init
flask db migrate -m "migration name"
flask db upgrade
```
# Run application

if already in /src
```python app.py```

else
```python src/app.py```

