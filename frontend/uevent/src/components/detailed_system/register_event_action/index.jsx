import React, { useState } from 'react';
import { useParams } from "react-router-dom";

const EventRegistrationButton = () => {
    const [registrationStatus, setRegistrationStatus] = useState(null);
    const [err, seterr] = useState(null);
    const { eventId } = useParams();
    const handleRegistration = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/detail/register/${eventId}`, {
                method: 'POST',
                mode: "cors",
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS',
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setRegistrationStatus(data);
            } else {
                const errorData = await response.json();
                const code = errorData.code;
                const message = errorData.error;
                seterr(`Bad Request: ${code} - ${message}`)
            }
        } catch (error) {
            // console.error(error.response);
            if (error.response) {
                if (error.response.request.status) {
                    const errorCode = error.response.request.status;
                    const errorMessage = error.response.data.error;
                    seterr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
                else if (error.response.data.code) {
                    const errorCode = error.response.data.code;
                    const errorMessage = error.response.request.statusText;
                    seterr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
            } else if (error.request) {
                seterr('No response received from the server. Please try again later.');
            } else {
                seterr('Error occurred while processing the request. Please try again later.');
            }
        }
    };

    return (
        <div>
            <div>
                {err && <div style={{ color: 'red' }}>{err}</div>}
            </div>
            <button onClick={handleRegistration}>Register for Event</button>
            {registrationStatus && (
                <p>
                    Registration Status: {registrationStatus.code} - {registrationStatus.msg || registrationStatus.error}
                </p>
            )}
        </div>
    );
};

export default EventRegistrationButton;
