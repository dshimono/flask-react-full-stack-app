import React from "react";

const Contactlist = ({ contacts, updateContact, updateCallback }) => {
    const prod = "https://flask-react-contacts-app.onrender.com/";
    const local = "http://127.0.0.1:5000/";
    let apiBackend = local;

    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE",
            };
            const response = await fetch(
                apiBackend + "delete_contact/${id}",
                options
            );
            if (response.status === 200) {
                updateCallback();
            } else {
                console.error("Failed to delete");
            }
        } catch (error) {
            alert(error);
        }
    };

    return (
        <div>
            <h2>Contacts</h2>
            <table>
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {contacts.map((contact) => (
                        <tr key={contact.id}>
                            <td>{contact.firstName}</td>
                            <td>{contact.lastName}</td>
                            <td>{contact.email}</td>
                            <td>
                                <button onClick={() => updateContact(contact)}>
                                    Update
                                </button>
                                <button onClick={() => onDelete(contact.id)}>
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Contactlist;
