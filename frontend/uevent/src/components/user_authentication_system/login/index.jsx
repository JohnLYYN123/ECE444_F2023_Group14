import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function LoginPage() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [err, seterr] = useState(null);

    const logInUser = () => {
        if (username.length === 0) {
            seterr("Username has left Blank!");
        }
        else if (password.length === 0) {
            seterr("Password has left Blank!");
        }
        else {
            axios.post('http://127.0.0.1:5000/user/login', {
                username: username,
                password: password
            })
                .then(function (response) {
                    console.log(response.data);
                    // navigate("/");
                })
                .catch(function (error) {
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
                });
        }
    }


    return (
        <>
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title text-center">Log Into Your Account</h5>
                                <div>
                                    {err && <div style={{ color: 'red' }}>{err}</div>}
                                </div>
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
        </>
    );
}