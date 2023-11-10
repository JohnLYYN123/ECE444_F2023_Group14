import React, { useState, useEffect } from 'react';
import axios from 'axios'
import { useParams } from "react-router-dom"
import 'bootstrap/dist/css/bootstrap.min.css';

export default function EventDetailPage() {
    const [eventDetail, setEventDetail] = useState(null);
    const [eventIdReq, setEventIdReq] = useState('');
    const [error, setError] = useState(null);
    const { eventId } = useParams();

    if(eventId.length === 0){
        console.log("empty eventId")
        throw new Error("invalid eventId [Empty eventId]")
    }

    const getEventDetail = async() => {
        axios.get(`http://127.0.0.1:5000/detail/view_detail?event_id=${eventId}`)
            .then(response => {
                const result = response.data;
                if (result.code !== 200){
                    // not successful operation
                    console.log("the request is not successful")
                    throw new Error("the operation is invalid")
                }

                if (result.msg !== 'OK'){
                    console.log(`the request is successful, but something
                        is not right, msg ${result.msg}`)
                    throw new Error(`Something is wrong, msg ${result.msg}`)
                }
                const data = result.data
                setEventDetail(data)
            })
            .catch(e => {
                console.log(e)
                throw new Error(`An error has occured ${e}`)
            });
    };
    return (
        <div>
            <h1></h1>
        </div>
    );
};