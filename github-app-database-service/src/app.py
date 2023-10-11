from flask import Flask
from config import Config
from models.models import db
from routes.user import user_routes
from routes.repository import repository_routes
from flask_migrate import Migrate, upgrade

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(user_routes)
app.register_blueprint(repository_routes)

migrate = Migrate(app, db)

PORT = os.getenv('PORT')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT) 