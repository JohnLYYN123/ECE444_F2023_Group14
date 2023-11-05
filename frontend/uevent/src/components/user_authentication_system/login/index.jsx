import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function LoginPage() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const logInUser = () => {
        if (username.length === 0) {
            alert("username has left Blank!");
        }
        else if (password.length === 0) {
            alert("password has left Blank!");
        }
        else {
            axios.post('http://127.0.0.1:5000/user/login', {
                username: username,
                password: password
            })
                .then(function (response) {
                    console.log(response);
                    // console.log(response.data);
                    // navigate("/");
                })
                .catch(function (error) {
                    console.log(error, 'error');
                    if (error.response.status === 401) {
                        alert("Invalid credentials");
                    } else if (error.response.status === 409) {
                        alert("Unauthorized Access");
                    } else if (error.response.status === 500) {
                        alert("Internal Server Error: " + error.response.data.error);
                    } else {
                        alert("An error occurred. Please try again later.");
                    }
                });
        }
    }


    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title text-center">Log Into Your Account</h5>
                            <form>
                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label">Username</label>
                                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" id="username" placeholder="Enter a valid username" />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">Password</label>
                                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="form-control" id="password" placeholder="Enter password" />
                                </div>
                                <div className="mb-3 form-check">
                                    <input type="checkbox" className="form-check-input" id="rememberMe" />
                                    <label className="form-check-label" htmlFor="rememberMe">Remember me</label>
                                </div>
                                <button type="button" className="btn btn-primary" onClick={logInUser}>Login</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}