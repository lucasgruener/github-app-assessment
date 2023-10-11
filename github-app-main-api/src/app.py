from flask import Flask
from github_routes import github_bp
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

app.register_blueprint(github_bp, url_prefix='/api')

PORT = os.getenv('PORT')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT) 