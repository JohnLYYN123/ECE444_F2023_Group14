import FilterSearcher from "./filterSearch";

export const filterTag = ['sport', 'art', 'travel', 'cooking'];
const FilterSearch = (props) => {

    const onFilterAction = (val) => {
        props.onFilter(val)
    };

    const filterTagContent = props.filterTag || filterTag;

    return <div className="filter">
        {filterTagContent.map((val) =>
        <FilterSearcher tagTitle={val} onFilter={() => onFilterAction(val)}/>)}
    </div>
}

export default FilterSearch;