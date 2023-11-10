import EventCard from "./eventCard";
import { useCallback } from "react";
import './eventCardTemplate.css';

const EventCardTemplate = (props) => {
    const {eventInfoArr} = props;
    const eventInfoCard = useCallback(() => {
        return eventInfoArr.map((item) => {
            return (<EventCard eventInfo={item}/>);

        });
    }, [eventInfoArr]);
    return <div className='eventCardTemplate'>
        {eventInfoCard()}
    </div>;
}

export default EventCardTemplate;