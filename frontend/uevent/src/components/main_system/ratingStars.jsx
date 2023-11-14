import React from 'react';
import { Rate } from 'antd';
const RatingStars = (props) => {
    return <Rate disabled defaultValue={props.averageRating}/>;
}
export default RatingStars;