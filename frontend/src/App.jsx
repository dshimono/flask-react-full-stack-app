import { useEffect, useState } from 'react';
import Contactlist from './ContactList';
import './App.css';

function App() {
const [contacts, setContacts] = useState([{'firstName': 'Denis', 'lastName': 'Shimono', 'email': 'dshimono@gmail.com', 'id': 1}])

useEffect(() => {
  // fetchContacts()
}, [])

  const fetchContacts = async () => {
    const response = await fetch('http://127.0.0.1:5000/contacts')
    const data = await response.json()
    setContacts(data.contacts)
    console.log(data.contacts)
  }

  return <Contactlist contacts={contacts}/>
}

export default App
