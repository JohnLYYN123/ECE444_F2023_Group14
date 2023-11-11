import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Enrollment = () => {
  const [enrolledEvents, setEnrolledEvents] = useState([]);
  const [viewingType, setViewingType] = useState('upcoming'); // defining the event state
  const [headerText, setHeaderText] = useState('You are viewing: Enrollment Cart');

  // Fetching events from backend
  const fetchEnrolledEvents = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/enrollment/userid?type=${viewingType}`);
      setEnrolledEvents(response.data);
    } catch (error) {
      console.error('Error during fetching enrolled events:', error);
    }
  };

  // Changing the Header Text
  const handleViewingTypeChange = (type) => {
    setViewingType(type);
    setHeaderText(`You are viewing: ${type === 'upcoming' ? 'Enrollment Cart' : 'Event History'}`);
  };

  useEffect(() => {
    fetchEnrolledEvents();
  }, [viewingType]); // fetch events for different event states

  return (
    <div>
      <h1>{headerText}</h1>

      {/* Switching between upcoming and past events */}
      <button onClick={() => handleViewingTypeChange('upcoming')}>Upcoming Events</button>
      <button onClick={() => handleViewingTypeChange('past')}>Past Events</button>

      {/* Display enrolled events */}
      <ul>
        {enrolledEvents.map((event) => (
          <li key={event.event_id}>{event.event_name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Enrollment;
