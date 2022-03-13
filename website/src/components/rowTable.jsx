const RowTable = (props) =>{
    return(Object.values(props.column).map(data => 
    <div className="col">{data}</div>
    ))
}; export default RowTable;