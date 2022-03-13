import ButtonSubmit from "./buttonSubmit";
import Input from "./input"


const TransactionCreate = (props) => {
    return (
        <div className="div_design container">
            <h3 className="padding_1">Create Transaction</h3>
              <div class="row">
                <div class="col">
                <label className="padding_1">The Sender ID:</label>
                <Input placeholder="Sender id" onChange={props.handelSender}></Input>
                </div>
                </div>
                <div class="row">
                <div class="col">
                <label className="padding_1">The Getter ID:</label>
                <Input placeholder="Getter id" onChange={props.handelGetter}></Input>
                </div>
                </div> 
                <div class="row">
                <div class="col">              
                <label className="padding_1">The Transactions:</label>
                <Input placeholder="Transaction" onChange={props.handelTransaction}></Input>
                </div>
                </div>

                <ButtonSubmit name="Create" handleSubmit={props.handelSubmit} ></ButtonSubmit>
        </div>
    )
}; export default TransactionCreate;