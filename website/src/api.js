const url = "http://localhost:5000/"
async function createTransaction(
                                    clientIDSender, 
                                    clientIDGetter, 
                                    totalTransaction,
                                    currentCurrency,
                                    converteCurrency){
    try{
    const data = {"client_id_sender":clientIDSender, "client_id_getter":clientIDGetter, 
    "total_transaction":totalTransaction, "current_currency":currentCurrency,
    "converte_currency":converteCurrency}
    const response = await fetch(url + "create/transaction/",{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    response = await response.json();
    console.log(response);
    }
    catch(error){
        console.error(error);
    }
}

