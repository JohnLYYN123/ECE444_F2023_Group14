import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from "react-router-dom";
import * as S from "./style";
import uevent from "../../../image/uevent.png"; // Import the image here

export default function LoginPage() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [err, setErr] = useState(null);

    const logInUser = () => {
        if (username.length === 0) {
            setErr("Username has been left blank!");
        } else if (password.length === 0) {
            setErr("Password has been left blank!");
        } else {
            axios.post('http://127.0.0.1:5000/user/login', {
                username: username,
                password: password
            })
                .then(async response => {
                    if (response.status === 200) {
                        const data = await response.data;
                        localStorage.setItem('token', data.token); // Store JWT token in local storage
                        console.log(`Log in successfully!`)
                        // Redirect to another page or perform other actions upon successful login if needed
                        window.location.href = '/';
                    } else {
                        const errorData = await response.json();
                        const code = errorData.code;
                        const message = errorData.error;
                        setErr(`Bad Request: ${code} - ${message}`)
                    }
                })
                .catch(function (error) {
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
                });
        }
    }


    return (
        <>
            <S.Container>
                <S.Img src={uevent} />
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <p style={{ marginRight: '10px' }}>Join</p>
                    {err && <div className="alert alert-danger">{err}</div>}
                </div>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="form-control"
                        id="username"
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="form-control"
                        id="password"
                    />
                </div>
                <S.DivButtons>
                    <S.ButtonSend onClick={logInUser}>Login</S.ButtonSend>
                </S.DivButtons>
                <S.DivRegister>
                    <S.LinkToRegister to="/register">
                        New here? <span>Create an Account</span>
                    </S.LinkToRegister>
                </S.DivRegister>
            </S.Container>
        </>
    );
}