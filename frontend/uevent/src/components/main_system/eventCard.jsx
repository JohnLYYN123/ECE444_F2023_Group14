import GeneralInfo from "./generalInfo";
import { Card } from "antd";
import "./eventCard.css";
import Filter from "./filter";

const EventCard = (props) => {
    return <>
        <div className="eventCard">
            <Card
                hoverable
                bordered={false}
                style={{ width: 500, borderRadius: 40}}
                cover={<img alt="example" src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png" />}
            >
                <GeneralInfo eventInfo={props.eventInfo}/>
                <div className="eventCard-filter">
                    <Filter filterTag={props.eventInfo.filterInfo}/>
                </div>
            </Card>
        </div>
    </>;
}

export default EventCard;