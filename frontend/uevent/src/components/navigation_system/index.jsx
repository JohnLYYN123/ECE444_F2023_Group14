import React, { useState } from 'react';



  const NavigationSystem = () => {

    const { userId } = useParams();

    const RedirectEnrollment = async () => {
      
      const response = await fetch('http://127.0.0.1:5000/enrollment/{userId}', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        
      });
  
      const data = await response.json();
      console.log(data); // Log the response from the server
    };
  
    const RedirectMain = async () => {
      
      const response = await fetch('http://127.0.0.1:5000/main_sys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        
      });
  
      const data = await response.json();
      console.log(data); // Log the response from the server
    };
  
    const RedirectLogout = async () => {
      
      const response = await fetch('http://127.0.0.1:5000/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      const data = await response.json();
      console.log(data); // Log the response from the server
    };
  
    return (
      <div>
        <button onClick={RedirectEnrollment}>Enrollment Cart</button>
        <button onClick={RedirectMain}>Main Page</button>
        <button onClick={RedirectLogout}>Logout</button>
      </div>
    );
  };
  
  export default NavigationSystem;
