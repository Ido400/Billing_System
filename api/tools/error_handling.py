class TransactionFailedError(Exception):
    pass

class CustomerNotFoundError(Exception):
    pass

class DeleteTransactionFailedError(Exception):
    pass

class GetTransactionsError(Exception):
    pass

class GetCustomersError(Exception):
    pass

class TransactionNotFoundError(Exception):
    pass

class UpdateTransactionFailed(Exception):
    pass

class FailedToCreateCustomers(Exception):
    pass

class KeyNotFound(Exception):
    pass