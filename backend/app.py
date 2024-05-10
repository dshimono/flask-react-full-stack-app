from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_smorest import Api
from models import Contact
from db import db
from dotenv import load_dotenv


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["API_TITLE"] = "Contacts List"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    db.init_app(app)


    @app.route("/")
    def hello_world():
        return "<p>Contact List server is up!</p>"

    @app.route("/contacts", methods=["GET"])
    def get_contacts():
        contacts = Contact.query.all()
        json_contacts = list(map(lambda x: x.to_json(), contacts))
        return jsonify({"contacts": json_contacts})

    @app.route("/create_contact", methods=["POST"])
    def create_contact():
        first_name = request.json.get("firstName")
        last_name = request.json.get("lastName")
        email = request.json.get("email")

        if not first_name or not last_name or not email:
            return (
                jsonify({"message": f"You must include a first name, last name and email.\nFirst name: {first_name}, \nLast name: {last_name}, \nEmail: {email}"}),
                400,
                )
        
        new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
        try:
            db.session.add(new_contact)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        return jsonify({"message": "User created."}), 201

    @app.route("/update_contact/<int:user_id>", methods=['POST', 'PATCH'])
    def update_contact(user_id):
        contact = Contact.query.get(user_id)

        if not contact:
            return jsonify({"message": "User not found."}), 404
        
        data =request.json
        contact.first_name = data.get("firstName", contact.first_name)
        contact.last_name = data.get("lastName", contact.last_name)
        contact.email = data.get("email", contact.email)

        db.session.commit()

        return jsonify({"message": "User updated."}), 200

    @app.route("/delete_contact/<int:user_id>", methods=['DELETE'])
    def delete_contact(user_id):
        contact = Contact.query.get(user_id)

        if not contact:
            return jsonify({"message": "User not found."}), 404

        try:
            db.session.delete(contact)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 400

        return jsonify({"message": "User deleted."}), 200


    if __name__ == "__main__":
        with app.app_context():
            db.create_all()

    return app