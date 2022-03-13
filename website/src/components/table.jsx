import ButtonTable from "./buttonTable";
import RowTable from "./rowTable";
import Input from "./input";

const Table = (props) =>{
    return <div className="div_design container">
        <h3 className="padding_1">Transaction Table</h3>
        <div className="row padding_1 row_top">
        {Object.keys(props.table[0]).map(data =>
             <div className="col">{data}</div>)}
             </div>
        {props.table.map(data =>
            <div className="row padding_1">
            {console.log(data)}
            <RowTable column={data}></RowTable>
            <Input onChange={props.onChangeTransactionUpdate} placeholder="New Transaction"></Input>
            <ButtonTable onClickHandel={props.handleUpdate} value={data["id"]} name="Update" ></ButtonTable>
            <ButtonTable onClickHandel={props.handleDelete} value={data["id"]} name="Delete"></ButtonTable>
            </div>
        )}
    </div>
}; export default Table;