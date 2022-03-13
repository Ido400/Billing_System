const TextBox = (props) =>{
    return <textarea  className="text_area" onChange={e => props.handleChange(e.target.value)}></textarea>;
};export default TextBox;

