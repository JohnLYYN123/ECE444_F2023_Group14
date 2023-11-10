import React, { useState, useEffect } from 'react';
import axios from 'axios'
import { useParams } from "react-router-dom"
import 'bootstrap/dist/css/bootstrap.min.css';
import "./display_event_detail.css";
import EventRegistrationButton from "../register_event_action"


export default function EventDetailPage() {
    const [eventDetail, setEventDetail] = useState(null);
    const [eventInfo, setEventInfo] = useState([]);
    const [commentInfo, setCommentInfo] = useState([]);
    const [detailReviewInfo, setDetailReviewInfo] = useState([]);
    const [eventIdReq, setEventIdReq] = useState('');
    const [error, setError] = useState(null);
    const { eventId } = useParams();

    if(eventId.length === 0){
        console.log("empty eventId")
        throw new Error("invalid eventId [Empty eventId]")
    }

    useEffect(() => {
        const GetEventDetail = async() => {
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
                const data = result.data;
                setEventDetail(data);
                setEventInfo(data.event_info);
                setCommentInfo(data.review_info);
                const review_d = commentInfo.review_detail;
                setDetailReviewInfo(review_d)
                console.log(data);
            })
            .catch(e => {
                console.log(e)
                throw new Error(`An error has occured ${e}`)
            })
        
        axios.get(`http://127.0.0.1:5000/detail/view_review_detail?event_id=${eventId}`)
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
                const data = result.data;
                setDetailReviewInfo(data)
                console.log(data);
            })
            .catch(e => {
                console.log(e)
                throw new Error(`An error has occured ${e}`)
            })
    };

    

    if (eventId !== 0 && eventId.length > 0) {
      GetEventDetail();
    }
    },[eventId]);

    return (
    <div className="controller">
        <div className="container-1">
            <div className="page-header">
                <h1>Event: {eventInfo.event_name}</h1>
                <h4>
                    Rating Score: {eventInfo.average_rating}<span class="subtitle-space"></span>
                    {eventInfo.number_rater} reviews<span class="subtitle-space"></span>
                    Address: 777 Bay St.<span class="subtitle-space"></span>
                </h4>
                <h4>
                    Club: {eventInfo.club_name}<span class="subtitle-space"></span>
                </h4>
            </div>
            <img src={eventInfo.event_image} width='800' height='300'></img>
                <div className="description-container">
                    <h5>Event Description: </h5>
                    <div>{eventInfo.event_description}</div>
                </div>

                <div className="Comment-Section">
                    <h5>Comments for the event</h5>
                        <ul>
                        {detailReviewInfo?.map((dict) => (
                            <li key={dict.review_id}>
                            <strong>Reviewer: </strong> {dict.review_user} <strong>   Rating for the event: </strong> {dict.rating} <strong>   Review Time: </strong> {dict.review_time} 
                            <div><strong>Comment: </strong> {dict.review_comment}</div>
                            </li>
                        ))}
                        </ul>
                </div>

        </div>
        <div className="card card-width">
            <img src="https://www.mymovingreviews.com/images/static-maps/static-map.php?center=Ontario,Toronto&zoom=12&size=620x300&maptype=roadmap&markers=icon:http:%2F%2Fwww.mymovingreviews.com%2Fimages%2Fmmrpin.png|shadow:true|Ontario,Toronto&sensor=false&visual_refresh=true&key=AIzaSyCFEGjaoZtuJwPI-0HBJQXHcJ1ElEN8btI"
                width='450' height='200'></img>
            <h3>Event Details</h3>
            <div className='image-icon'>
                <img src="https://static.vecteezy.com/system/resources/previews/000/440/310/original/vector-calendar-icon.jpg"
                width="30" height="30">
                </img>
                <span className="subtitle-space">{eventInfo.event_time}</span>
            </div>
            <div className='image-icon'>
                <img src="https://www.pngfind.com/pngs/m/114-1147878_location-poi-pin-marker-position-red-map-google.png"
                width="30" height="30"></img>
                <span className="subtitle-space">Exam Center</span>
            </div>
            <div className='image-icon'>
                <img src="https://cdn0.iconfinder.com/data/icons/money-icons-rounded/110/Wallet-1024.png"
                width="30" height="30">
                </img>
                <span className="subtitle-space">$ {eventInfo.charge} CAD</span>
            </div>
            <div className="button-icon">
                <EventRegistrationButton parameter={eventInfo.event_id}/>
            </div>
        </div>
    </div>
    );
};