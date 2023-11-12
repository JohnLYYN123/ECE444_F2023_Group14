import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Button, Alert } from 'react-bootstrap';

const EventRegistrationButton = () => {
    const [registrationStatus, setRegistrationStatus] = useState(null);
    const [err, setErr] = useState(null);
    const { eventId } = useParams();

    const handleRegistration = async () => {
        try {
            const response = await axios.post(
                `http://127.0.0.1:5000/detail/register/${eventId}/`,
                null,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `${window.localStorage['token']}`,
                    },
                }
            );

            if (response.status === 200) {
                setRegistrationStatus({ code: 200, msg: 'Registration successful!' });
                setErr(null);
            } else {
                const errorData = response.data;
                const code = errorData.code;
                const message = errorData.error || 'Unknown error';
                if (code == "401" & message == "Authentication is required to access this resource") {
                    // Redirect to the homepage or another desired page
                    alert('Please log in to continue.');
                    window.location.href = '/login';
                }
                setErr(`Bad Request: ${code} - ${message}`);
                setRegistrationStatus(null);
            }
        } catch (error) {
            // console.error(error.response);
            if (error.response) {
                if (error.response.request.status) {
                    const errorCode = error.response.request.status;
                    const errorMessage = error.response.data.error;
                    setErr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
                else if (error.response.data.code) {
                    const errorCode = error.response.data.code;
                    const errorMessage = error.response.request.statusText;
                    setErr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
            } else if (error.request) {
                setErr('No response received from the server. Please try again later.');
            } else {
                setErr('Error occurred while processing the request. Please try again later.');
            }
            setRegistrationStatus(null);
        }
    };

    return (
        <div className="registration-container">
            <Button variant="primary" onClick={handleRegistration} className="registration-button">
                Register for Event
            </Button>

            <div className="my-4" />

            {err && (
                <Alert variant="danger" className="error-message">
                    {err}
                </Alert>
            )}

            <div className="my-4" />

            {registrationStatus && (
                <Alert variant="success" className="success-message">
                    {registrationStatus.msg}
                </Alert>
            )}
        </div>
    );
};

export default EventRegistrationButton;
