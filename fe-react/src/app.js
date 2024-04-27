import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [coordinates, setCoordinates] = useState({ lat: 0, lng: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      fetchCoordinates();
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const fetchCoordinates = () => {
    axios.get('http://localhost:5000/map_data')
      .then(response => {
        setCoordinates(response.data);
      })
      .catch(error => {
        console.error('Error fetching coordinates:', error);
      });
  };

  return (
    <div className="App">
      <h1>Map</h1>
      <p>Latitude: {coordinates.lat}</p>
      <p>Longitude: {coordinates.lng}</p>
    </div>
  );
}

export default App;
