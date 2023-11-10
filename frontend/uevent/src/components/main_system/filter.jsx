import FilterTag from "./filterTag";

export const filterTag = ['sport', 'art', 'travel', 'cooking'];
const Filter = (props) => {
    const filterTagContent = props.filterTag || filterTag;
    return <div className="filter">
        {filterTagContent.map((value) => <FilterTag tagTitle={value}/>)}
    </div>;
}

export default Filter;