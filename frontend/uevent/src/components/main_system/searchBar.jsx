import { Input } from 'antd';
const { Search } = Input;

const SearchBar = (props) => {
    return <>
        <Search
            placeholder="input search text"
            allowClear
            enterButton="Search"
            size="large"
            onSearch={props.onSearch}
        />
    </>;
}

export default SearchBar;