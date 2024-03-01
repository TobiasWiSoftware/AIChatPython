import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

import Chat from "./pages/Chat";
import Upload from "./pages/Upload";


function App() {
  useEffect(() => {
    const isFirstVisit = localStorage.getItem('isFirstVisit') === null;

    if (isFirstVisit) {
      // Using fetch to make the API call
      fetch('/delete_all_data', {
        method: 'POST', // Specify the method
        headers: {
          // Add any required headers here
          'Content-Type': 'application/json',
        },
        // If you need to send a body, uncomment and modify the line below
        // body: JSON.stringify({ your: "data" }),
      })
      .then(response => {
        if (response.ok) {
          return response.json(); // or .text() or .blob() etc. depending on your response
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        console.log('Data successfully deleted on first visit.');
        localStorage.setItem('isFirstVisit', 'false');
      })
      .catch(error => {
        console.error('Error deleting data on first visit:', error);
      });
    }
  }, []); // This effect runs only once on component mount

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
