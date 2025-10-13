from flask import Flask
from app.funct import init_db
from app.routes import routes
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.secret_key = 'thorecainedestept'
    app.register_blueprint(routes)
    init_db()
    return app
