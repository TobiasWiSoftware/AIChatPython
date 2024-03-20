import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

import Chat from "./pages/Chat";
import Upload from "./pages/Upload";



function App() {
  useEffect(() => {
    // Placeholder for future logic
    console.log('Component did mount.');
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
