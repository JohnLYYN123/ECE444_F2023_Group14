import { Space, Tag, Button } from "antd";
import './filterTag.css'
const FilterTag = (props) => {
    return <Space wrap>
        <Tag className='filterTag'>{props.tagTitle}</Tag>
    </Space>
}

export default FilterTag;