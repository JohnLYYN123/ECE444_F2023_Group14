import React, {useState, useEffect, useRef, useCallback} from 'react';
import { Button } from "antd";
import {HomeOutlined, UserOutlined} from '@ant-design/icons';
import { Alert } from 'react-bootstrap';
import axios from 'axios';
import { useParams, Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./display_event_detail.css";
import EventRegistrationButton from "../register_event_action";
import NavigationButton from "../nav_button";
import PostCommentAndRatingForm from "../add_new_comment";
import { Container, Card } from 'react-bootstrap';
import RatingStars from "../../main_system/ratingStars";
import locationIcon from "../../../assets/icons/location.png";


export default function EventDetailPage() {
    const [eventDetail, setEventDetail] = useState(null);
    const [eventInfo, setEventInfo] = useState([]);
    const [commentInfo, setCommentInfo] = useState([]);
    const [detailReviewInfo, setDetailReviewInfo] = useState([]);
    const [eventIdReq, setEventIdReq] = useState('');
    const [error, setError] = useState(null);
    const { eventId } = useParams();


    if (eventId.length === 0) {
        console.log("empty eventId")
        throw new Error("invalid eventId [Empty eventId]")
    }

    useEffect(() => {
        const GetEventDetail = async () => {
            axios.get(`https://ece444uevent.pythonanywhere.com/detail/view_detail?event_id=${eventId}`, {
                mode: "cors",
                method: 'GET',
                body: null,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`,
                    'Access-Control-Allow-Origin': '*',
                }
            })
                .then(response => {
                    console.log("response", response)

                    const result = response.data;
                    if (result.code !== 200) {
                        // not successful operation
                        console.log("the request is not successful")
                        throw new Error("the operation is invalid")
                    }

                    if (result.msg !== 'OK') {
                        console.log(`the request is successful, but something
                        is not right, msg ${result.msg}`)
                        throw new Error(`Something is wrong, msg ${result.msg}`)
                    }
                    const data = result.data;
                    setEventDetail(data);
                    setEventInfo(data.event_info);
                    setAverageRating(data.event_info.average_rating);
                    setCommentInfo(data.review_info);
                    const review_d = commentInfo.review_detail;
                    setDetailReviewInfo(review_d)
                    console.log(data);
                })
                .catch(e => {
                    console.log(e)
                    alert('Please log in to continue.');
                    window.location.href = '/login'
                })

            axios.get(`https://ece444uevent.pythonanywhere.com/detail/view_review_detail?event_id=${eventId}`, {
                mode: "cors",
                method: 'GET',
                body: null,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`,
                    'Access-Control-Allow-Origin': '*',
                }
            })
                .then(response => {
                    const result = response.data;
                    if (result.code !== 200) {
                        // not successful operation
                        console.log("the request is not successful")
                        throw new Error("the operation is invalid")
                    }

                    if (result.msg !== 'OK') {
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
                    alert('Please log in to continue.');
                    window.location.href = '/login'
                })
        };

        if (eventId !== 0 && eventId.length > 0) {
            GetEventDetail();
        }
    }, [eventId]);

    const ratingProvider = useCallback(() => {
        return averageRating === -1 ? <></> : <RatingStars averageRating={averageRating}/>
    }, [averageRating]);

    return (
        <div className="detail-page">
            <div className="detail-page-header">
                <Link to="../../">
                    <Button type="primary" icon={<HomeOutlined />}>MAIN PAGE</Button>
                </Link>
                <h1>{eventInfo.event_name}</h1>
            </div>
            <img className="detail-image" src={eventInfo.event_image} alt='Event Image'/>
            <div className="detail-page-info">
                <div className="detail-page-content">
                    <div className="detail-page-content-scroll">
                        <div id="home" className="home">
                            {ratingProvider()}
                            <div className="number-rater">
                                {eventInfo.number_rater} reviews <UserOutlined />
                            </div>
                        </div>
                        <div className="detail-event-sections">
                            <div className="detail-event-section">
                                <div className="detail-event-section-title">Address</div>
                                <div className="detail-event-section-content">
                                    <img src={locationIcon} style={{height: "20px"}}/>
                                    {eventInfo.address}
                                </div>
                            </div>
                            <div className="detail-event-section">
                                <div className="detail-event-section-title">Club Information</div>

                                <div className="detail-event-section-content">
                                    {eventInfo.club_name}:<>   </>
                                    {eventInfo.club_desc}
                                </div>
                            </div>
                            <div className="detail-event-section">
                                <div className="detail-event-section-title">Event Description</div>
                                <div className="detail-event-section-content">{eventInfo.event_description}</div>
                            </div>


                            <div className="detail-event-section">
                                <div className="detail-event-section-title">Comments & Reviews</div>
                                <div id="comment" className="comment">
                                    <div className="Comment-Section">
                                    {detailReviewInfo?.map((dict) => (
                                        <Card className="comment-card" key={dict.review_id}>
                                            <div className="rating">
                                                <RatingStars averageRating={dict.rating}/>
                                            </div>
                                            <div className="comment">
                                                {dict.review_comment}
                                            </div>

                                            <div className="lastRow">
                                                <div>
                                                    {dict.review_time}
                                                </div>
                                                <div className="reviewer">
                                                    {`by ${dict.review_user}`}
                                                </div>
                                            </div>

                                        </Card>
                                    ))}

                                </div>
                                </div>
                            </div>

                            <div className="detail-event-section">
                                <div className="detail-event-section-title">Leave your Comment and Rating</div>
                                <div className="comment-form">
                                    <PostCommentAndRatingForm idx={eventInfo.event_id} />
                                </div>
                            </div>
                        </div>

                    </div>
                </div>


                <div className="card card-width">
                    <img src="https://www.mymovingreviews.com/images/static-maps/static-map.php?center=Ontario,Toronto&zoom=12&size=620x300&maptype=roadmap&markers=icon:http:%2F%2Fwww.mymovingreviews.com%2Fimages%2Fmmrpin.png|shadow:true|Ontario,Toronto&sensor=false&visual_refresh=true&key=AIzaSyCFEGjaoZtuJwPI-0HBJQXHcJ1ElEN8btI"
                         className="card-img"></img>
                    <div className="card-content">
                        <h3>Event Details</h3>

                        <div className="card-content-detail">
                            <div className='image-icon'>
                                <img src="https://static.vecteezy.com/system/resources/previews/000/440/310/original/vector-calendar-icon.jpg"
                                     width="30" height="30">
                                </img>
                                <span className="subtitle-space">{eventInfo.event_time}</span>
                            </div>
                            <div className='image-icon'>
                                <img src="https://www.pngfind.com/pngs/m/114-1147878_location-poi-pin-marker-position-red-map-google.png"
                                     width="30" height="30"></img>
                                <span className="subtitle-space">{eventInfo.position_address}</span>
                            </div>
                            <div className='image-icon'>
                                <img src="https://cdn0.iconfinder.com/data/icons/money-icons-rounded/110/Wallet-1024.png"
                                     width="30" height="30">
                                </img>
                                <span className="subtitle-space">$ {eventInfo.charge} CAD</span>
                            </div>
                        </div>
                        <div className="button-icon">
                            <EventRegistrationButton idx={eventInfo.event_id} />
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};