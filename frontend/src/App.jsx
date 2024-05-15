import { useEffect, useState } from "react";
import Contactlist from "./ContactList";
import "./App.css";
import ContactForm from "./ContactForm";

const prod = "https://flask-react-contacts-app.onrender.com/";
const local = "http://127.0.0.1:5000/";
export let apiBackend = local;

function App() {
    const [contacts, setContacts] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentContact, setCurrentContact] = useState({});

    useEffect(() => {
        fetchContacts();
    }, []);

    const fetchContacts = async () => {
        const response = await fetch(apiBackend + "contacts");
        const data = await response.json();
        setContacts(data.contacts);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setCurrentContact({});
    };

    const openCreateModel = () => {
        if (!isModalOpen) setIsModalOpen(true);
    };

    const openEditModal = (contact) => {
        if (isModalOpen) return;
        setCurrentContact(contact);
        setIsModalOpen(true);
    };

    const onUpdate = () => {
        closeModal();
        fetchContacts();
    };
    return (
        <>
            <Contactlist
                contacts={contacts}
                updateContact={openEditModal}
                updateCallback={onUpdate}
            />
            <button onClick={openCreateModel}>Create New Contact</button>
            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>
                            &times;
                        </span>
                        <ContactForm
                            existingContact={currentContact}
                            updateCallback={onUpdate}
                        />
                    </div>
                </div>
            )}
        </>
    );
}

export default App;
