import React from 'react';
import { Rate } from 'antd';
const RatingStars = (props) => <Rate disabled defaultValue={props.averageRating} />;
export default RatingStars;