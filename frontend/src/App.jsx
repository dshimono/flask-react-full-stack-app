import { useEffect, useState } from "react";
import Contactlist from "./ContactList";
import "./App.css";
import ContactForm from "./ContactForm";

// "http://localhost:5000" for local dev;
// the "import.meta.env" (Vite) should be replaced by "process.env" in Create React App.
export const apiBackend = import.meta.env.VITE_REACT_APP_API_BACKEND;

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
