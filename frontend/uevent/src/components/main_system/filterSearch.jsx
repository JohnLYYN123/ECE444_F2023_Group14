import { Space, Button } from "antd";
import './filterTag.css'
const FilterSearcher = (props) => {
    return <Space wrap>
        <Button className='filterTag' type='primary' onClick={props.onFilter}>{props.tagTitle}</Button>
    </Space>
}

export default FilterSearcher;