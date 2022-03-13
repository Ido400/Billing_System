
const ButtonSubmit = (props) =>{
    return <div className="div_center"><button className="button_sce" onClick={props.handleSubmit}>{props.name}</button></div>;
}; export default ButtonSubmit;