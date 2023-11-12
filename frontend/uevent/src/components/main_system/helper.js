export const fetchData = async (event_id) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys?event_id=${event_id}`);
        if (res.status === 200) {
            const eventInfo = await res.json();
            return eventInfo;
        }
        else {
            alert('Please log in to continue.');
            window.location.href = '/login'
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
        else {
            alert('Please log in to continue.');
            window.location.href = '/login'
        }

    } catch (e) {
        console.log(e);
    }
}

export const filterSearch = async (filter_key) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys/filter?title=${filter_key}`, {
            mode: "cors",
            method: 'GET',
            body: null,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${window.localStorage['token']}`,
                'Access-Control-Allow-Origin': '*',
            }
        });
        if (res.status === 200) {
            const eventInfo = await res.json();
            return eventInfo;
        }
        else {
            alert('Please log in to continue.');
            window.location.href = '/login'
        }
    } catch (e) {
        console.log(e);
    }
}