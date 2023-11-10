import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useParams } from "react-router-dom";
import axios from 'axios';

export default function PostCommentAndRatingForm() {

    const [username, setUsername] = useState('');
    const [comment, setComment] = useState('');
    const [rating, setRating] = useState('');
    const [err, setErr] = useState(null);
    const { eventId } = useParams();

    const handleOptionChange = (event) => {
        setRating(event.target.value);
    };

    const submit = () => {
        if (username.length === 0) {
            setErr("Username has been left blank!");
        } else if (comment.length === 0) {
            setErr("Comment has been left blank!");
        } else if (rating.length === 0) {
            setErr("Rating has been left blank!");
        } else if (rating != '1' && rating == '2' && rating == '3' && rating == '4' && rating == '5') {
            setErr("Rating must be a number between 1 to 5!");
        } else {
            axios.post(`http://127.0.0.1:5000/detail/add_comment?event_id=${eventId}`, {
                username: username,
                comment: comment,
                rating: rating
            })
                .then(async response => {
                    if (response.status === 200) {
                        const data = await response.data;
                        localStorage.setItem('data', data.response_data);
                        console.log(`Commented successfully!`)
                        // Redirect to main display page

                    } else {
                        const errorData = await response.data;
                        const code = errorData.code;
                        const message = errorData.response_data;
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
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title text-center">Make Your Comment!</h5>
                                <div>
                                    {err && <div style={{ color: 'red' }}>{err}</div>}
                                </div>
                                <form>
                                    <div className="mb-3">
                                        <label htmlFor="username" className="form-label">Your username</label>
                                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" id="username" />
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="comment" className="form-label">Add Your Comment</label>
                                        <textarea type="comment" value={comment} onChange={(e) => setComment(e.target.value)} className="form-control" id="comment" rows="5"/>
                                    </div>
                                    {/* <div className="mb-3">
                                        <label htmlFor="rating" className="form-label">Add Your Rating: Number 1 to 5</label>
                                        <input type="text" value={rating} onChange={(e) => setRating(e.target.value)} className="form-control" id="rating" />
                                    </div> */}


                                    <div>
                                        <label htmlFor="rating">Your Rating:&nbsp;&nbsp;&nbsp;</label>
                                        <select type="text" id="rating" value={rating} onChange={(e) => setRating(e.target.value)} className="form-control">
                                            <option value='1'>1 Star</option>
                                            <option value='2'>2 Star</option>
                                            <option value='3'>3 Star</option>
                                            <option value='4'>4 Star</option>
                                            <option value='5'>5 Star</option>
                                        </select>
                                        <p>Selected option: {rating}</p>
                                    </div>


                                    <div className="text-center">
                                        <button type="button" className="btn btn-primary" onClick={submit}>Submit</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}


