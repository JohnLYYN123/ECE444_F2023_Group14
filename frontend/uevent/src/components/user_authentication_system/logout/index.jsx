import React, { useState } from 'react';

const Logout = () => {
    const [err, seterr] = useState(null);

    const handleLogout = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/user/logout', {
                mode: "cors",
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`
                },
            });

            if (response.ok) {
                console.log('Logout successful');
                window.localStorage.removeItem("token");
                // Redirect to the homepage or another desired page
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                const code = errorData.code;
                const message = errorData.error;
                seterr(`Bad Request: ${code} - ${message}`)
            }
        } catch (error) {
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
        <>
            <div>
                {err && <div style={{ color: 'red' }}>{err}</div>}
            </div>
            <div className="logout-page">
                <h2>Logout</h2>
                <p>Are you sure you want to log out?</p>
                <button onClick={handleLogout}>Logout</button>
            </div>
        </>
    );
};

export default Logout;
