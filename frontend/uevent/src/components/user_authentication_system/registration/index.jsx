import React, { useState } from 'react';
import { Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as S from "./style";
import uevent from "../../../image/uevent.png"; // Import the image here

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
            const response = await fetch('http://127.0.0.1:5000/user/register', {
                method: 'POST',
                body: JSON.stringify(formData),
                mode: "cors",
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const data = await response.json();
                window.localStorage.setItem("token", data.token);
                console.log('Thank you, you registered successfully!')
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                const code = errorData.code;
                const message = errorData.error;
                seterr(`Bad Request: ${code} - ${message}`)
            }
        } catch (error) {
            console.error(error);
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
            <div className="container mt-5">
                <div className="col-md-6 offset-md-3">
                    <div className="card">
                        <S.Img src={uevent} />
                        <div className="card-body">
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <h3 style={{ marginRight: '10px' }}>Register</h3>
                                {err && <div className="alert alert-danger">{err}</div>}
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
                                <S.DivButtons>
                                    <S.ButtonBack to="/">Back</S.ButtonBack>
                                    <S.ButtonSend type="submit">Register</S.ButtonSend>
                                </S.DivButtons>
                                <S.DivSingIn>
                                    <S.LinkToLogin to="/login">
                                        Already Have an Account? <span>Sign in</span>
                                    </S.LinkToLogin>
                                </S.DivSingIn>
                            </Form>
                        </div>
                    </div>
                </div>
            </div>
        </>

    )
}

export default RegisterForm;