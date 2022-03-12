from tools.calculator import Calculator
from tools.error_handling import TransactionFailedError, CustomerNotFoundError
from tools.error_handling import DeleteTransactionFailedError,GetTransactionsError
from tools.error_handling import TransactionNotFoundError
from tools.error_handling import UpdateTransactionFailed

class ManageTransactions:
    def __init__(self, sql_contoller:object) -> None:
        """
        Args:
        -----
            sql_controller(SqlDB): The sql object that controll the db
        """
        self.sql_controller = sql_contoller
    
    def create_transaction(self, 
                                client_id_sender:str, 
                                client_id_getter:str, 
                                total_transaction:float, 
                                current_currency:str, 
                                converte_currency:str):
        """
        This method will create a new transaction and it will do all
        the calculation for converting the currency and add/sub from
        the totals.

        Args:
        -----
            client_id_sender(str): The customer id of the sender
            client_id_getter(str): The customer id of the getter
            total_transaction(float): The total transaction
            current_currency(str): The currency of the sender
            converte_currency(str): The currency of the getter
        """
        try:
            customer_sender_total, customer_getter_total = self.get_customer_total(
                                                            client_id_sender,
                                                            client_id_getter)
            cal = Calculator(
                                customer_sender_total, 
                                customer_getter_total, 
                                total_transaction, 
                                current_currency, 
                                converte_currency)
        
            self.sql_controller.create_transaction(
                                                    client_id_sender, 
                                                    client_id_getter, 
                                                    cal.sub_total_sender(), 
                                                    cal.add_total_getter(),
                                                    total_transaction,
                                                    current_currency,
                                                    cal.convert_money(), 
                                                    converte_currency)
        except TransactionFailedError:
            raise TransactionFailedError("Failed to create transaction")
        except CustomerNotFoundError:
             raise CustomerNotFoundError("The customers are not found")

    def update_transaction(self, transaction_id:int, total_transaction:float):
        """
        This method will change the total transaction and it will reset
        to last totals and calculate again the new totals.

        Args:
        -----
            transaction_id(int): The id of the transaction
            total_transaction(float): The new total transaction
        """
        try:
            trans = self.sql_controller.get_transaction(transaction_id)
            customer_sender_total, customer_getter_total = self.reset_transaction( 
                                                            trans["user_id_transac"],
                                                            trans["user_id_get"], 
                                                            trans["total_before_convert"],
                                                            trans["currency_user_transac"],
                                                            trans["currency_user_get"])
            cal = Calculator(
                            customer_sender_total, 
                            customer_getter_total, 
                            total_transaction, 
                            trans["currency_user_transac"], 
                            trans["currency_user_get"])
            
            self.sql_controller.update_transaction(
                                                trans["user_id_transac"], 
                                                trans["user_id_get"],  
                                                cal.sub_total_sender(), 
                                                cal.add_total_getter(),
                                                transaction_id, 
                                                total_transaction,  
                                                trans["currency_user_transac"],
                                                cal.convert_money(),
                                                trans["currency_user_get"])
        except UpdateTransactionFailed:
            raise UpdateTransactionFailed(f"failed to update the transaction \
                                            {transaction_id}")
        except TransactionNotFoundError:
            raise TransactionNotFoundError(f"can't find the transaction \
                                            {transaction_id}")
        except CustomerNotFoundError:
            raise UpdateTransactionFailed(f"failed to update the transaction \
                                            {transaction_id}")
        
    
    def delete_transaction(self, transaction_id:int):
        """
        This method will delete the transaction and reset the totals.

        Args:
        -----
            transaction_id(int): The transaction id
        """
        try:
            trans = self.sql_controller.get_transaction(transaction_id)
            customer_sender_total, customer_getter_total = self.reset_transaction( 
                                                            trans["user_id_transac"],
                                                            trans["user_id_get"], 
                                                            trans["total_before_convert"],
                                                            trans["currency_user_transac"],
                                                            trans["currency_user_get"])
            
            self.sql_controller.delete_transaction( transaction_id,
                                                    trans["user_id_transac"], 
                                                    trans["user_id_get"], 
                                                    customer_sender_total,
                                                    customer_getter_total)
        except DeleteTransactionFailedError:
            raise DeleteTransactionFailedError("Unable to delete transaction")
        except TransactionNotFoundError:
            raise TransactionNotFoundError(f"Transaction not found {transaction_id}")
        except CustomerNotFoundError:
            raise DeleteTransactionFailedError("Unable to delete transaction")
    
    def get_all_transaction(self) -> list:
        """
        This method will return a list of dicts of transactions

        Return:
        -------
            Return list of dicts of transactions
        """
        try:
            transactions  = []
            for transaction in self.sql_controller.get_transactions():
                transactions.append(transaction.__dict__)
            return transactions
        except GetTransactionsError:
            raise GetTransactionsError("Can't get the transaction")

    def reset_transaction(self,client_id_sender:str, 
                                            client_id_getter:str, 
                                            total_transaction:float,
                                            current_currency:str, 
                                            converte_currency:str) -> tuple:
        """
        This method will reset the total of the two customers and it
        will return there last totals.

        Return:
        -------
            Return a tuple of the last totals
        """
        try:
            client_sender_total, client_getter_total = self.get_customer_total(
                                                            client_id_sender,
                                                            client_id_getter)
            cal = Calculator(
                                client_sender_total, 
                                client_getter_total, 
                                total_transaction, 
                                current_currency, 
                                converte_currency)

            return (cal.add_total_sender(), cal.sub_total_getter())
        except CustomerNotFoundError:
            raise CustomerNotFoundError(f"Can't find the customers")

    def get_customer_total(self, client_id_sender, client_id_getter)->tuple:
        """
        This method will retrun the totals of the two customers

        Return:
        -------
            Return the total of the two customers
        """
        try:
            customer_sender_total = self.sql_controller.get_customer(client_id_sender)["total_price"]
            customer_getter_total = self.sql_controller.get_customer(client_id_getter)["total_price"]
            return (customer_sender_total, customer_getter_total)
        except CustomerNotFoundError:
            raise CustomerNotFoundError(f"Can't find the customers ids")