from currency_converter import CurrencyConverter

class Calculator:
    """
    This object will calculate the total and converte the currency
    """
    def __init__(self, 
                        total_sender:float, 
                        total_getter:float, 
                        total_transaction:float, 
                        transaction_currency:str, 
                        converte_currency:str) -> None:
        """
        Args:
        -----
            total_sender(float): the total of the sender
            total_getter(float): the total of the getter
            total_transaction(float): the total transaction
            transaction_currency(str): the sender currency
            converte_currency(str): the getter currency
        """
        self.total_sender = total_sender 
        self.total_getter = total_getter
        self.total_transaction = total_transaction
        self.transaction_currency = transaction_currency
        self.converte_currency = converte_currency

    def convert_money(self) ->float:
        """
        This method will converte the total_transaction into the
        converte currency

        Return:
        -------
            Return float number 
        """
        if(self.transaction_currency != self.converte_currency):
            c = CurrencyConverter()
            convert_total = c.convert(  self.total_transaction, 
                                        self.transaction_currency, 
                                        self.converte_currency)
            return convert_total
        return self.total_transaction
    
    def sub_total_sender(self):
        """
        Return:
        -------
            Return the sub of the sender total and his transaction
        """
        return self.total_sender - self.total_transaction
    
    def add_total_getter(self):
        """
        Return:
        -------
            Return the add of the getter total and the converte money
            he gets.
        """
        return self.total_getter + self.convert_money()

    def add_total_sender(self):
        """
        Return:
        -------
            Return the add of the sender total and his transaction
        """
        return self.total_sender + self.total_transaction
    
    def sub_total_getter(self):
        """
        Return:
        -------
            Return the sub of the getter total and the converte money
            he gets.
        """
        return self.total_getter - self.convert_money()