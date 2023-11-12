import {useCallback, useEffect, useState} from "react";
import EventCardTemplate from "../main_system/eventCardTemplate";
import EventInfoDataProvider from "../main_system/eventInfoDataProvider";
import { fetchEnrollData } from "./helper";
import { Tabs } from "antd";
import './enrollment_cart_system.css';


const EnrollmentCart = () => {
    const [enrollInfoArr, setEnrollInfoArr] = useState([]);
    const [pastEnrollInfoArr, setPastEnrollInfoArr] = useState([]);
    const [tabSelected, setTabSelected] = useState('1');

    useEffect(() => {
        Promise.resolve(fetchEnrollData()).then((res) => {
            if (res?.future && res.future.length > 0) {
                const enrollInfoLocal = []
                const enrollInfoRes = res.future;
                enrollInfoRes.forEach((e) => {
                    enrollInfoLocal.push(new EventInfoDataProvider(
                        e.event_id,
                        e.event_name,
                        e.event_time,
                        e.average_rating,
                        e.event_image,
                        e.filter_info
                    ));
                });
                console.log('current', enrollInfoLocal)
                setEnrollInfoArr(enrollInfoLocal);
            }
            if (res?.pass && res.pass.length > 0) {
                const enrollPastInfoLocal = []
                const enrollPastInfoRes = res.pass;
                enrollPastInfoRes.forEach((e) => {
                    enrollPastInfoLocal.push(new EventInfoDataProvider(
                        e.event_id,
                        e.event_name,
                        e.event_time,
                        e.average_rating,
                        e.event_image,
                        e.filter_info
                    ));
                });
                console.log('past', enrollPastInfoRes)
                setPastEnrollInfoArr(enrollPastInfoLocal);
            }
        });


    }, [setEnrollInfoArr, setPastEnrollInfoArr])

    const onChange = useCallback((key) => {
        setTabSelected(key);
    }, []);

    const items = [
        {
            key: '1',
            label: 'Enrolled',
            children: <EventCardTemplate eventInfoArr={enrollInfoArr} />,
        },
        {
            key: '2',
            label: 'Passed',
            children: <EventCardTemplate eventInfoArr={pastEnrollInfoArr} />,
        },
    ];

    return <>
        <div className="enroll-tabs">
            <Tabs defaultActiveKey="1" items={items} onChange={onChange} />
        </div>
    </>
};

export default EnrollmentCart;


