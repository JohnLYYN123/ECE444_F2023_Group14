import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const PostEventForm = () => {
    const [eventData, setEventData] = useState({
        event_name: '',
        event_time: '',
        event_description: '',
        address: '',
        fee: '',
        // shared_title: '',
        // shared_image: '',
        club_name: ''
    });
    const [clubNames, setClubNames] = useState([]);

    const [err, seterr] = useState(null);

    // Fetch club names when the component mounts
    useEffect(() => {
        fetch('/main_sys/allClubs')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => setClubNames(data))
            .catch(error => {
                console.error('Error fetching club names:', error);
            });
    }, []);


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/main_sys/add/event', {
                mode: "cors",
                method: 'POST',
                body: JSON.stringify(eventData),
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`,
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'
                },
            });
            if (response.ok) {
                console.log('Post club successfullly!');
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
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEventData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    return (
        <>
            <div className="container mt-5">
                <div className="col-md-6 offset-md-3">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="mb-4">Register</h2>
                            {err && <div className="alert alert-danger">{err}</div>}
                            <Form onSubmit={handleSubmit}>
                                <Form.Group controlId="event_name">
                                    <Form.Label>Event Name</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="event_name"
                                        value={eventData.event_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </Form.Group>

                                <Form.Group controlId="event_time">
                                    <Form.Label>Event Time</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="event_time"
                                        value={eventData.event_time}
                                        onChange={handleChange}
                                        required
                                    />
                                </Form.Group>

                                <Form.Group controlId="event_description">
                                    <Form.Label>Event Description</Form.Label>
                                    <Form.Control
                                        as="textarea"
                                        name="event_description"
                                        value={eventData.event_description}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Form.Group controlId="address">
                                    <Form.Label>Address</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="address"
                                        value={eventData.address}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Form.Group controlId="fee">
                                    <Form.Label>Fee</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="fee"
                                        value={eventData.fee}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                {/* <Form.Group controlId="shared_title">
                                    <Form.Label>Shared Title</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="shared_title"
                                        value={eventData.shared_title}
                                        onChange={handleChange}
                                    />
                                </Form.Group>

                                <Form.Group controlId="shared_image">
                                    <Form.Label>Shared Image</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="shared_image"
                                        value={eventData.shared_image}
                                        onChange={handleChange}
                                    />
                                </Form.Group> */}

                                <Form.Group controlId="club_name">
                                    <Form.Label>Club Name</Form.Label>
                                    <Form.Control
                                        as="select"
                                        name="club_name"
                                        value={eventData.club_name}
                                        onChange={handleChange} // Update club_name in the state when user selects a club
                                        required
                                    >
                                        <option value="">Select a club</option>
                                        {clubNames.map((club, index) => (
                                            <option key={index} value={club}>
                                                {club}
                                            </option>
                                        ))}
                                    </Form.Control>
                                </Form.Group>
                                <div className="text-center">
                                    <Button variant="primary" type="submit" >
                                        Post the event
                                    </Button>
                                </div>
                            </Form>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default PostEventForm;
