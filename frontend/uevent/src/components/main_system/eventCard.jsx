import GeneralInfo from "./generalInfo";
import { Card } from "antd";
import "./eventCard.css";
import Filter from "./filter";
import { Link } from 'react-router-dom';

const EventCard = (props) => {
    return <>
        <div className="eventCard">
        <Link to={`../event_detail/${props.eventInfo._eventId}`}>
            <Card
                hoverable
                bordered={false}
                style={{ width: 300, borderRadius: 40, minHeight: 330}}
                cover={<img className="event-image" alt="example" src={
                    props.eventInfo.eventImage || "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
                }/>}
            >
                <GeneralInfo eventInfo={props.eventInfo}/>
                <div className="eventCard-filter">
                    <Filter filterTag={props.eventInfo.filterInfo}/>
                </div>
            </Card>
            </Link>
        </div>
    </>;
}

export default EventCard;