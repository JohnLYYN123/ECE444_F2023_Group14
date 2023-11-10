export const fetchData = async (event_id) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys?event_id=${event_id}`);
        if (res.status === 200) {
            const eventInfo = await res.json();
            return eventInfo;
        }

    } catch (e) {
        console.log(e);
    }
}

export const searchData = async (search_string) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys/search?value=${search_string}`);
        if (res.status === 200) {
            const eventInfo = await res.json();
            return eventInfo;
        }

    } catch (e) {
        console.log(e);
    }
}