import os 
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_smorest import Api, abort

from models import ContactModel
from db import db
from dotenv import load_dotenv

from resources.contact import blp as ContactBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///mydatabase.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE EXECPTIONS"] = True
    app.config["API_TITLE"] = "Contacts List API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-documentation"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    
    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ContactBlueprint)

    @app.route("/")
    def hello_world():
        return "<h1>Welcome to Contacts API</h1>"        

    return app