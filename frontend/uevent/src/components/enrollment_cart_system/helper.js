export const fetchEnrollData = async () => {
    try {
        const res = await fetch(`http://localhost:5000/enroll/`, {
            mode: "cors",
            method: 'GET',
            body: null,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${window.localStorage['token']}`,
                'Access-Control-Allow-Origin': '*',
            }
        });

        // console.log('res', res);

        if (res.status === 200) {
            const enrollInfo = await res.json();
            return enrollInfo;
        }

    } catch (e) {
        console.log(e);
    }
}
