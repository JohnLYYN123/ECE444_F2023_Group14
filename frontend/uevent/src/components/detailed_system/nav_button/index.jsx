import React from 'react';
import { Link } from 'react-router-dom';

const NavigationButton = ({ to, buttonText, eventid }) => {
    const linkWithParam = eventid ? `${to}/${eventid}` : to;
    return (
        <Link to={linkWithParam}>
            <button>{buttonText}</button>
        </Link>
    );
};

export default NavigationButton;