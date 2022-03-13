const ButtonTable = (props) =>{
    return <button className="button_sce" onClick={() => props.onClickHandel(props.value)}>{props.name}</button>
}; export default ButtonTable;