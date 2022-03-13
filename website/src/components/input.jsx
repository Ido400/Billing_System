const Input = (props) => {
    return <input onChange={e => props.onChange(e.target.value)} placeholder={props.placeholder}></input>;
}; export default Input;