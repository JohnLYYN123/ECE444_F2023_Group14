import RatingStars from "./ratingStars";
import './generalInfo.css'

const GeneralInfo = (props) => {
    const { eventName, eventTime, averageRating } = props.eventInfo;
    return <>
        <div>
            <div className="eventTitle">{eventName}</div>
            <div className="eventTime">{eventTime}</div>
        </div>
        <RatingStars averageRating={averageRating}/>

    </>
}

export default GeneralInfo;