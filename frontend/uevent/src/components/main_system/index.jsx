import SearchBar from './searchBar';
import Filter from './filter';
import EventCardTemplate from './eventCardTemplate';
import {useCallback, useEffect, useState} from 'react';
import EventInfoDataProvider from './eventInfoDataProvider';
import './mainSystem.css';
import {fetchData, searchData} from "./helper";


const MainPage = () => {
    const [eventInfoArr, setEventInfoArr] = useState([])

    useEffect( () => {

        Promise.resolve(fetchData(-1)).then((res) => {
            if (res?.data && res.data.length > 0) {
                const eventInfoResLocal = []
                const eventInfoRes = res.data;
                eventInfoRes.forEach((e) => {
                    eventInfoResLocal.push(new EventInfoDataProvider(
                        e.event_id,
                        e.event_name,
                        e.event_time,
                        e.average_rating,
                        e.event_image,
                        e.filter_info
                    ));
                });
                setEventInfoArr(eventInfoResLocal);
            }
        });
    }, [setEventInfoArr]);

    const eventCardTemplateProvider = useCallback(() => {

        return <EventCardTemplate eventInfoArr={eventInfoArr}/>
    }, [eventInfoArr])


    const onSearch = useCallback((value, _e) => {
        if (value === '') {
            Promise.resolve(fetchData(-1)).then((res) => {
                if (res?.data && res.data.length > 0) {
                    const eventInfoResLocal = []
                    const eventInfoRes = res.data;
                    eventInfoRes.forEach((e) => {
                        eventInfoResLocal.push(new EventInfoDataProvider(
                            e.event_id,
                            e.event_name,
                            e.event_time,
                            e.average_rating,
                            e.event_image,
                            e.filter_info
                        ));
                    });
                    setEventInfoArr(eventInfoResLocal);
                }
            });
        } else {
            Promise.resolve(searchData(value)).then((res) => {
                if (res?.data && res.data.length > 0) {
                    const eventInfoResLocal = []
                    const eventInfoRes = res.data;
                    eventInfoRes.forEach((e) => {
                        eventInfoResLocal.push(new EventInfoDataProvider(
                            e.event_id,
                            e.event_name,
                            e.event_time,
                            e.average_rating,
                            e.event_image,
                            e.filter_info
                        ));
                    });
                    setEventInfoArr(eventInfoResLocal);
                }
            });

        }

    }, [setEventInfoArr]);

    return <>
        <div className="mainPage">
            <SearchBar onSearch={onSearch}/>
            <div className="mainPage-filter">
                <Filter/>
            </div>
            {eventCardTemplateProvider()}
        </div>
    </>;
}
export default MainPage;