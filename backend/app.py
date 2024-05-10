from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_smorest import Api, abort
from models import Contact
from db import db
from dotenv import load_dotenv

from resources.contacts import blp as ContactsBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE EXECPTIONS"] = True
    app.config["API_TITLE"] = "Contacts List"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/api-documentation"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    db.init_app(app)

    api = Api(app)
    api. register_blueprint(ContactsBlueprint)


    @app.route("/")
    def hello_world():
        return "<h1>Welcome to Contacts API</h1>"        

    if __name__ == "__main__":
        with app.app_context():
            db.create_all()

    return app