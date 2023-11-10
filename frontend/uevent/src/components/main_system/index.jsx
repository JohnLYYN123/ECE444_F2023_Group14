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
        // const eventInfoArrMock = [
        //     new EventInfoDataProvider(
        //         'eventName 1', 'event is fun', '2023-10-2', '2', '20'),
        //     new EventInfoDataProvider(
        //         'eventName 2', 'event is more fun', '2023-10-3', '4', '20')];
        // setEventInfoArr(eventInfoArrMock);

        Promise.resolve(fetchData(-1)).then((res) => {
            console.log('then', res)
            if (res?.data && res.data.length > 0) {
                const eventInfoResLocal = []
                const eventInfoRes = res.data;
                eventInfoRes.forEach((e) => {
                    console.log(e);
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
        console.log('search',value);
        if (value === '') {
            Promise.resolve(fetchData(-1)).then((res) => {
                console.log('then', res)
                if (res?.data && res.data.length > 0) {
                    const eventInfoResLocal = []
                    const eventInfoRes = res.data;
                    eventInfoRes.forEach((e) => {
                        console.log(e);
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
            console.log('then', res)
            if (res?.data && res.data.length > 0) {
                const eventInfoResLocal = []
                const eventInfoRes = res.data;
                eventInfoRes.forEach((e) => {
                    console.log(e);
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