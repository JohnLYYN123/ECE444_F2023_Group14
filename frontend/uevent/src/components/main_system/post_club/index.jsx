import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function PostClub() {

    const [clubName, setClubName] = useState('');
    const [description, setDescription] = useState('');
    const [err, seterr] = useState(null);

    const post_club = async () => {
        try {
            const data = {
                club_name: clubName,
                description: description
            };
            const response = await fetch('http://127.0.0.1:5000/main_sys/add/club', {
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
                console.log('Post club successfullly!');
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
    }


    return (
        <>
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title text-center">Post club</h5>
                                <div>
                                    {err && <div style={{ color: 'red' }}>{err}</div>}
                                </div>
                                <form>
                                    <div className="mb-3">
                                        <label htmlFor="clubName" className="form-label">Club Name</label>
                                        <input
                                            type="text"
                                            value={clubName}
                                            onChange={(e) => setClubName(e.target.value)}
                                            className="form-control"
                                            id="clubName"
                                            placeholder="Enter a club name"
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="description" className="form-label">Description</label>
                                        <textarea
                                            value={description}
                                            onChange={(e) => setDescription(e.target.value)}
                                            className="form-control"
                                            id="description"
                                            placeholder="Enter description"
                                            rows="4" // You can adjust the number of rows as needed
                                        />
                                    </div>
                                    <button type="button" className="btn btn-primary" onClick={post_club}>Post the club</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}