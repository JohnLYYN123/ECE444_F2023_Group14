export const fetchData = async (event_id) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys/?event_id=${event_id}`, {
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
            window.location.href = '/login'
        }

    } catch (e) {
        console.log("catch")
    }
}

export const searchData = async (search_string) => {
    try {
        const res = await fetch(`http://localhost:5000/main_sys/search?value=${search_string}`, {
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
        else{
            window.location.href = '/login'
        }
    } catch (e) {
        console.log(e);
    }
}