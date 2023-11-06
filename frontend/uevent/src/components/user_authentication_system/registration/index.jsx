import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        uoftEmail: '',
        password: '',
        uoftStudentId: '',
        firstName: '',
        lastName: '',
        department: '',
        enrolledTime: '',
        organizationalRole: false,
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };
    const [err, seterr] = useState(null);

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/user/register', formData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log(response.data);
        } catch (error) {
            console.error(error.response);
            if (error.response) {
                if (error.response.data.code) {
                    const errorCode = error.response.data.code;
                    const errorMessage = error.response.data.error;
                    seterr(`Bad Request: ${errorCode} - ${errorMessage}`)
                } else if (error.response.request.status) {
                    const errorCode = error.response.request.status;
                    const errorMessage = error.response.data.error;
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
            <Form onSubmit={handleFormSubmit}>
                <Form.Group controlId="formUsername">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formUofTEmail">
                    <Form.Label>UofT Email</Form.Label>
                    <Form.Control
                        type="email"
                        name="uoftEmail"
                        value={formData.uoftEmail}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formUofTStudentId">
                    <Form.Label>UofT Student ID</Form.Label>
                    <Form.Control
                        type="text"
                        name="uoftStudentId"
                        value={formData.uoftStudentId}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formFirstName">
                    <Form.Label>First Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formLastName">
                    <Form.Label>Last Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formDepartment">
                    <Form.Label>Department</Form.Label>
                    <Form.Control
                        type="text"
                        name="department"
                        value={formData.department}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formEnrolledTime">
                    <Form.Label>Enrolled Time</Form.Label>
                    <Form.Control
                        type="text"
                        name="enrolledTime"
                        value={formData.enrolledTime}
                        onChange={handleInputChange}
                    />
                </Form.Group>

                <Form.Group controlId="formOrganizationalRole">
                    <Form.Check
                        type="checkbox"
                        label="Organizational Role"
                        name="organizationalRole"
                        checked={formData.organizationalRole}
                        onChange={(e) => setFormData({ ...formData, organizationalRole: e.target.checked })}
                    />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </>

    )
}

export default RegisterForm;