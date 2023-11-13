
import { useCallback, useEffect, useState } from "react";
import EventCardTemplate from "../main_system/eventCardTemplate";
import EventInfoDataProvider from "../main_system/eventInfoDataProvider";
import { fetchEnrollData } from "./helper";
import { Tabs } from "antd";
import './enrollment_cart_system.css';
import Toast from 'react-bootstrap/Toast';
import Col from 'react-bootstrap/Col';

const EnrollmentCart = () => {
    const [enrollInfoArr, setEnrollInfoArr] = useState([]);
    const [pastEnrollInfoArr, setPastEnrollInfoArr] = useState([]);
    const [tabSelected, setTabSelected] = useState('1');
    const [showB, setShowB] = useState(true);
    const [showA, setShowA] = useState(true);

    const toggleShowA = () => setShowA(!showA);
    const toggleShowB = () => setShowB(!showB);

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
                // console.log('current', enrollInfoLocal)
                setEnrollInfoArr(enrollInfoLocal);
            }
            if (res?.past && res.past.length > 0) {
                const enrollPastInfoLocal = []
                const enrollPastInfoRes = res.past;
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
                // console.log('past', enrollPastInfoRes)
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
            children: enrollInfoArr.length > 0 ? (
                <EventCardTemplate eventInfoArr={enrollInfoArr} />
            ) : (
                <>
                    <Col md={6} className="mb-2 ms-3 ">
                        <Toast show={showA} onClose={toggleShowA}>
                            <Toast.Header>
                                <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
                                <strong className="me-auto">Uevent</strong>
                            </Toast.Header>
                            <Toast.Body>Hello, you haven't enroll any new events yet.</Toast.Body>
                        </Toast>
                    </Col>
                </>
            ),
        },
        {
            key: '2',
            label: 'Passed',
            children: pastEnrollInfoArr.length > 0 ? (
                <EventCardTemplate eventInfoArr={pastEnrollInfoArr} />
            ) : (
                <>
                    <Col md={6} className="mb-2  ms-3 ">

                        <Toast onClose={toggleShowB} show={showB}>
                            <Toast.Header>
                                <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
                                <strong className="me-auto">Uevent</strong>
                            </Toast.Header>
                            <Toast.Body>Hello, you didn't enroll any past events.</Toast.Body>
                        </Toast>
                    </Col>
                </>
            ),
        },
    ];

    return <>
        <div className="enroll-tabs">
            <Tabs defaultActiveKey="1" items={items} onChange={onChange} />
        </div>
    </>
};

export default EnrollmentCart;


