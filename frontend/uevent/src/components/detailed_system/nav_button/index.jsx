import React from 'react';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NavigationButton = ({ to, buttonText, eventid }) => {
    const linkWithParam = eventid ? `${to}/${eventid}` : to;
    return (
        <Link to={linkWithParam}>
            <Button variant="primary">{buttonText}</Button>
        </Link>
    );
};

export default NavigationButton;