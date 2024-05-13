from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from db import db
from models import ContactModel
from schemas import ContactSchema

blp = Blueprint("contacts", __name__, description="Operations on contacts")

def add_update_contact(new_contact):
    try:
        db.session.add(new_contact)
        db.session.commit()  
    except IntegrityError:
        abort(
            400,
            message="Missing required fiels or a contact with this email already exists."
        )
    except KeyError:
        abort(
            500,
            message=f"An error occurred creating contact. Error message: {KeyError}"
        )

@blp.route("/contacts")
class ContactsList(MethodView):
    @blp.response(200, ContactSchema(many=True))
    def get(self):
        schema = ContactSchema(many=True)
        contact_list = schema.dump(ContactModel.query.all())
        return jsonify({"contacts": contact_list})

    @blp.arguments(ContactSchema)
    @blp.response(200, ContactSchema)
    def post(self, contact_data):
        new_contact = ContactModel(**contact_data)
        add_update_contact(new_contact)
        return jsonify({"message": "Contact created."})


@blp.route("/contact/<int:user_id>")
class Contact(MethodView):

    @blp.arguments(ContactSchema)
    def patch(self, contact_data, user_id):
        contact_data = ContactModel.query.get_or_404(user_id)       

        new_data = request.json
        contact_data.firstName = new_data.get("firstName", contact_data.firstName)
        contact_data.lastName = new_data.get("lastName", contact_data.lastName)
        contact_data.email = new_data.get("email", contact_data.email)

        add_update_contact(contact_data)

        return jsonify({"message": "Contact updated."})
    
    def delete(self, user_id):
        contact = ContactModel.query.get_or_404(user_id)
        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contact deleted."}
