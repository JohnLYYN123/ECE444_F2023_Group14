import React, { useState } from 'react';
import { Button, Alert, Container, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const Logout = () => {
    const [err, seterr] = useState(null);

    const handleLogout = async () => {
        try {
            const response = await fetch('https://ece444uevent.pythonanywhere.com/user/logout', {
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
                window.location.href = '/login';
                alert('Thank you for your visiting');
            } else {
                const errorData = await response.json();
                const code = errorData.code;
                const message = errorData.error || 'Unknown error';
                if (code == "401" & message == "Authentication is required to access this resource") {
                    // Redirect to the homepage or another desired page
                    alert('Please log in to continue.');
                    window.location.href = '/login';
                }
                seterr(`Bad Request: ${code} - ${message}`)
            }
        } catch (error) {
            if (error.response) {
                if (error.response.request.status) {
                    console.log("You need to log in first")
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
            {/* <Container className="d-flex justify-content-center align-items-center vh-100">
                <Card style={{ width: '18rem' }}>
                    <Card.Body>
                        <Card.Title>Logout</Card.Title>
                        <Card.Text>
                            Are you sure you want to log out?
                        </Card.Text>
                        {err && <Alert variant="danger">{err}</Alert>}
                        <div className="text-center mt-3">
                            <Button variant="primary" onClick={handleLogout}>Logout</Button>
                        </div>
                    </Card.Body>
                </Card>
            </Container> */}
            <Button variant="primary" onClick={handleLogout}>
                Logout
                {/* {err && <Alert variant="danger" className="ml-2">{err}</Alert>} */}
            </Button>
        </>
    );
};

export default Logout;
