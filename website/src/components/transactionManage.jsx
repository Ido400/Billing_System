import React, { Component } from 'react';
import Table from './table';
import TransactionCreate from './transactionCreate';

class TransactionManage extends Component {
    state={
        table:[],
        transaction:"",
        getterID:"",
        senderID:"",
        transaction_update:""
    }
    render() {
        if(this.state.table.length == 0){
            return <div>
                <TransactionCreate customers={this.state.customers} 
                                handelSender={this.handelChangeSender} 
                                handelGetter={this.handelChangeGetter} 
                                handelTransaction={this.handelChangeTransaction}
                                handelSubmit={this.handelSubmitTransaction}></TransactionCreate>
            </div>
        }
       
        return (
            <div>
                <TransactionCreate customers={this.state.customers} 
                            handelSender={this.handelChangeSender} 
                            handelGetter={this.handelChangeGetter} 
                            handelTransaction={this.handelChangeTransaction}
                            handelSubmit={this.handelSubmitTransaction}></TransactionCreate>
            <div>
                <Table 
                    onChangeTransactionUpdate={this.handelTransactionUpdate}
                    handleUpdate={this.handelUpdate} 
                    table={this.state.table} 
                    handleDelete={this.handelDelete}>   
                    </Table>
            </div>
           
            
            </div>
        );
    }
    componentDidMount = async () =>{
        /*
        This method will fetch the transactions when the component 
        was mount
         */
        await this.fetchTransactions()
    }
    handelDelete = async (data) => {
        /*
        This method will handel the delete button

        Args:
        -----
            data(string): The transaction id
         */
        console.log("The transaction id: " + data)
        await this.deleteTransaction(data)
    }

    handelChangeGetter = (data) => {
        /*
        This method will handel the input of the getter id

        Args:
        -----
            data(string): The id of the getter 
         */
        this.setState({getterID:data})
    }

    handelChangeSender = (data) => {
        /*
        This method will handel the input of the sender id

        Args:
        -----
            data(string): The id of the sender
         */

        this.setState({senderID:data})
    }   
   
    handelTransactionUpdate = (data) =>{
        /*
        This method will handel the transaction update input

        Args:
        -----
            data(string): The transaction number
         */
        data = this.convertToFloat(data)
        if(data !== ""){
            this.setState({transaction_update:data})
            return
        }
    }

    handelChangeTransaction = (data) =>{
        /*
        This method will handel the transaction input
        
        Args:
        -----
            data(string): The transaction number
         */
        data = this.convertToFloat(data)
        if(data !== ""){
            console.log(data)
            this.setState({transaction:data})
            return
        }

        console.error("Unable to set state data is not number");

    }

    handelSubmitTransaction = () =>{
        /*
        This method will call the create transaction function 
         */
        if(this.state.transaction != "" && this.state.getterID != "" && this.state.senderID != ""){
            let data = {client_id_sender:this.state.senderID,
                        client_id_getter:this.state.getterID,
                        total_transaction:this.state.transaction}
            if(this.state.getterID === this.state.senderID){
                console.error("The id is the same");
                return
            }
            
            this.createTransaction(data)
        }
        else{
            console.error("Data is missing");
        }
    }

    convertToFloat = (data) =>{
        /*
        This method will convert the data into float number

        Args:
        -----
            data(string): The transaction input
         */
        const new_data = parseFloat(data)
        if(isNaN(new_data)){
            console.error("Cant convert data");
            return ""
        }
        return new_data
     
    }

    handelUpdate = async (data) => {
        /*
        This method will update the transaction 

        Args:
        -----
            data(string): The transaction id
         */
        console.log("update id: " + data)
        if(this.state.transaction_update !=""){
            await this.updateTransaction(data,this.state.transaction_update)
            return
        }
        console.error("Failed to update");
    }

    fetchTransactions = async () => {
        /*
        This method will fetch the transactions
         */
        try{
            const response = await fetch(this.props.url + "/get/transactions")
            const data = await response.json()
            if(typeof(data) != 'object'){
                console.error("Invalid Data: " + data);
                return
        }
        this.setState({table:data})
        }
        catch (error){
            console.error(error);
        }
    }

    deleteTransaction = async (transactionId) => {
        /*
        This method will delete the transaction 
         */
        const data = {"transaction_id" : transactionId};
        try{
        let response = await fetch(this.props.url + "/delete/transaction", {
                                method: 'DELETE',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(data)});
        response = response.json()
        console.log(response);
        }
        catch (error){
            console.error(error);
        }
    }

    updateTransaction = async (transactionId, totalTransaction) =>{
        /*
        This method will update the transaction
         */
        const data = {"transaction_id":transactionId, "total_transaction":totalTransaction}
        try{
            let response = await fetch(this.props.url + "/update/transaction", {
                                    method: 'POST',
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify(data)});
            response = response.json()
            console.log(response);
            }
        catch (error){
                console.error(error);
        }
    }

   
    createTransaction = async (data) =>{
        /*
        This method will create new transaction
         */
        try{
            const response = await fetch(this.props.url + "/create/transaction",{
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)});
            response = await response.json()
            console.log(response)
        }
        catch(error){
            console.error("unable to create transaction " + error);
        }
    }

}

export default TransactionManage;