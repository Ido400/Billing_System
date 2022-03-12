from tools.error_handling import CustomerNotFoundError, FailedToCreateCustomers


class ManageCustomers:
    def __init__(self, sql_controller) -> None:
        """
        Args:
        -----
            sql_controller(SqlDB): the sql controller object
        """
        self.sql_controller = sql_controller
    def get_customers(self) -> list:
        """
        This method will fetch all the customers and return
        a list of customers in dict.

        Retrun:
        -------
            Return a list of dicts customers
        """
        try:
            customers = []
            for customer in self.sql_controller.get_customers():
                customers.append(customer.__dict__)
            return customers
        except CustomerNotFoundError:
            raise CustomerNotFoundError("The customers not found")
        
    def insert_customers(self, customers):
        """
        This method will insert customers into customer
        table.

        Args:
        -----
            customers(list): list of the dicts customers
        """
        try:
            for customer in customers:
                self.sql_controller.insert_customer(
                                        customer["customer_id"],
                                        customer["first_name"],
                                        customer["last_name"],
                                        customer["email"],
                                        customer["gender"],
                                        customer["country"],
                                        customer["city"],
                                        customer["street"],
                                        customer["phone"],
                                        float(customer["total_price"]),
                                        customer["currency"],
                                        customer["cerdit_card_type"],
                                        customer["cerdit_card_number"])
        except FailedToCreateCustomers:
            raise FailedToCreateCustomers("Failed to create customers")