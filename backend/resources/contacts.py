from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Contact
from db import db


blp = Blueprint("contacts", __name__, description="Operations on contacts")

@blp.route("/contacts")
class Contacts(MethodView):
    def get(self):
        try:
            contacts = Contact.query.all()
            json_contacts = list(map(lambda x: x.to_json(), contacts))
            return jsonify({"contacts": json_contacts})
        except KeyError:
            abort(404, message=f"List of contacts not found. Error: {KeyError}")

@blp.route("/create_contact")
class CreateContacts(MethodView):
    def post(self):
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
            return jsonify({"message": "User created."}), 201
        except Exception as error:
            abort(400, message= f"Error: {str(error)}")


@blp.route("/update_contact/<int:user_id>")
class UpadateContact(MethodView):
    def patch(self, user_id):
        contact = Contact.query.get(user_id)

        if not contact:
            abort(404, {"message": "User not found."})
        
        data =request.json
        contact.first_name = data.get("firstName", contact.first_name)
        contact.last_name = data.get("lastName", contact.last_name)
        contact.email = data.get("email", contact.email)

        db.session.commit()

        return jsonify({"message": "User updated."}), 200
    

@blp.route("/delete_contact/<int:user_id>")
class DeleteContact(MethodView):
    def delete(self, user_id):
        contact = Contact.query.get(user_id)

        if not contact:
            return jsonify({"message": "User not found."}), 404

        try:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({"message": "User deleted."}), 200
        except Exception as error:
            abort(jsonify({"message": str(error)}))
