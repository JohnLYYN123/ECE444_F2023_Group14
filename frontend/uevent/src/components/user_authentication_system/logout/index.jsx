import React from 'react';

const Logout = () => {

    const handleLogout = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/user/logout', {
                mode: "cors",
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `${window.localStorage['token']}`
                },
            });

            if (response.ok) {
                console.log('Logout successful');
                window.localStorage.removeItem("token");
                // Redirect to the homepage or another desired page
                window.location.href = '/';
            } else {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('Error occurred during logout:', error);
        }
    };

    return (
        <div className="logout-page">
            <h2>Logout</h2>
            <p>Are you sure you want to log out?</p>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Logout;
