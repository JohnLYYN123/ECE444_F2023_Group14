import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Button, Alert } from 'react-bootstrap';
import uevent from "../../../image/uevent.png"; // Import the image here
import * as S from "./style";

export default function PostClub() {

    const [clubName, setClubName] = useState('');
    const [description, setDescription] = useState('');
    const [err, setErr] = useState(null);
    const [success, setSucess] = useState(null);

    const post_club = async () => {
        try {
            if (clubName.length === 0) {
                setErr("Club name has been left blank!");
            } else if (description.length === 0) {
                setErr("Description has been left blank!");
            } else {
                const data = {
                    club_name: clubName,
                    description: description
                };
                const response = await fetch('https://ece444uevent.pythonanywhere.com/main_sys/add/club', {
                    mode: "cors",
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `${window.localStorage['token']}`,
                        'Access-Control-Allow-Origin': '*',
                    },
                });
                if (response.ok) {
                    // console.log('Post club successfullly!');
                    setErr(null);
                    setSucess(`Congratulations, you post the club successfully!`)
                } else {
                    const errorData = await response.json();
                    const code = errorData.code;
                    const message = errorData.error || 'Unknown error';
                    if (code == "401" & message == "Authentication is required to access this resource") {
                        // Redirect to the homepage or another desired page
                        alert('Please log in to continue.');
                        window.location.href = '/login';
                    }
                    setSucess(null);
                    setErr(`Bad Request: ${code} - ${message}`)
                }
            }
        } catch (error) {
            console.error(error.response);
            if (error.response) {
                if (error.response.request.status) {
                    const errorCode = error.response.request.status;
                    const errorMessage = error.response.data.error;
                    setSucess(null);
                    setErr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
                else if (error.response.data.code) {
                    const errorCode = error.response.data.code;
                    const errorMessage = error.response.request.statusText;
                    setSucess(null);
                    setErr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
            } else if (error.request) {
                setSucess(null);
                setErr('No response received from the server. Please try again later.');
            } else {
                setSucess(null);
                setErr('Error occurred while processing the request. Please try again later.');
            }
        }
    }


    return (
        <>
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <S.Img src={uevent} />
                            <div className="card-body">
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <h3 style={{ marginRight: '10px' }}>New Club?</h3>
                                    {success && <Alert variant="success">{success}</Alert>}
                                    {err && <Alert variant="danger">{err}</Alert>}
                                </div>
                                <Form>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="clubName">Club Name</Form.Label>
                                        <Form.Control
                                            type="text"
                                            value={clubName}
                                            onChange={(e) => setClubName(e.target.value)}
                                            id="clubName"
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="description">Description</Form.Label>
                                        <Form.Control
                                            as="textarea"
                                            value={description}
                                            onChange={(e) => setDescription(e.target.value)}
                                            id="description"
                                            rows={4}
                                        />
                                    </Form.Group>
                                    <S.DivButtons>
                                        <Button variant="primary" type="button" onClick={post_club}>
                                            Post the club
                                        </Button>
                                    </S.DivButtons>
                                </Form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}