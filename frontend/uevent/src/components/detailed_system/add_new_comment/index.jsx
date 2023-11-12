import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useParams } from "react-router-dom";
import axios from 'axios';

export default function PostCommentAndRatingForm() {

    const [comment, setComment] = useState('');
    const [rating, setRating] = useState('5');
    const [err, setErr] = useState(null);
    const { eventId } = useParams();

    const handleOptionChange = (event) => {
        setRating(event.target.value);
    };

    const submit = async () => {

        if (comment.length === 0) {
            setErr("Comment has been left blank!");
        } else if (rating.length === 0) {
            setErr("Rating has been left blank!");
        } else if (rating != '1' && rating == '2' && rating == '3' && rating == '4' && rating == '5') {
            setErr("Rating must be a number between 1 to 5!");
        } else {
            try {
                const data = {
                    comment: comment,
                    rating: rating,
                };
                const response = await fetch(`http://127.0.0.1:5000/detail/add_comment?event_id=${eventId}`, {
                    mode: "cors",
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `${window.localStorage['token']}`,
                        'Access-Control-Allow-Origin': '*',
                    },
                });
                // Handle the response as needed
                console.log(response);
            } catch (error) {
                // Handle errors
                console.error("Error:", error);
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
                                <h5 className="card-title text-center">Make Your Comment!</h5>
                                <div>
                                    {err && <div style={{ color: 'red' }}>{err}</div>}
                                </div>
                                <form>
                                    <div className="mb-3">
                                        <label htmlFor="comment" className="form-label">Add Your Comment</label>
                                        <textarea type="comment" value={comment} onChange={(e) => setComment(e.target.value)} className="form-control" id="comment" rows="5" />
                                    </div>
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


