from os import abort, environ

from flask import Flask, request, jsonify
from flask_cors import CORS

from tools.error_handling import FailedToCreateCustomers
from tools.manage_customers import ManageCustomers
from tools.manage_transaction import ManageTransactions
from tools.sql_controller import SqlDB
from tools.error_handling import TransactionFailedError, CustomerNotFoundError
from tools.error_handling import DeleteTransactionFailedError,GetTransactionsError
from tools.error_handling import GetCustomersError, TransactionNotFoundError
from tools.error_handling import UpdateTransactionFailed
from tools.logger_controller import Logger

app = Flask(__name__)

CORS(app)

SQL_HOSTNAME=environ["SQL_HOSTNAME"]
SQL_USERNAME=environ["SQL_USERNAME"]
SQL_PASSWORD=environ["SQL_PASSWORD"]
SQL_DATABASE=environ["SQL_DATABASE"]
SQL_TYPE = "mysql+pymysql"

LOGGER = Logger("api")

sql_controller = SqlDB(SQL_USERNAME, SQL_PASSWORD,SQL_HOSTNAME, 
                        SQL_DATABASE, SQL_TYPE, LOGGER)

manage_transaction = ManageTransactions(sql_controller)

manage_customers = ManageCustomers(sql_controller)

@app.route("/create/transaction", methods=["POST"])
def create_transaction():
    """
    request = {"client_id_sender":"", "client_id_getter":"", 
                "total_transaction":0.0}
    This method will create new transaction
    """
    try:
        data = request.get_json()
        manage_transaction.create_transaction(  data["client_id_sender"],
                                                data["client_id_getter"],
                                                data["total_transaction"])
        return jsonify("Success to do the transaction"), 200
    except TransactionFailedError:
        abort(500, description="Failed to do transaction")  
    except CustomerNotFoundError:
        abort(404, description="Customer not found")


@app.route("/update/transaction", methods=["POST"])
def update_transaction():
    """
    request = {"transaction_id":0, "total_transaction":0.0}

    This method will update the transaction
    """
    try:
        data = request.get_json()
        manage_transaction.update_transaction(  data["transaction_id"],
                                                data["total_transaction"])
        return jsonify("Updating Successfully"), 200
    except UpdateTransactionFailed:
        abort(500, description="Failed to update transaction")
    except TransactionNotFoundError:
        abort(404, description="Transaction not found")   

@app.route("/delete/transaction", methods=["DELETE"])
def delete_transaction():
    """
    request = {"transaction_id":0}

    This method will delete the transaction
    """
    try:
        data = request.get_json()
        manage_transaction.delete_transaction(data["transaction_id"])
        return jsonify("Delete Successfully"), 200
    except DeleteTransactionFailedError:
        abort(500, description="Failed to delete the transaction")
    except TransactionNotFoundError:
        abort(404, description="Transaction not found")

@app.route("/get/transactions", methods=["GET"])
def get_transactions() ->list:
    """
    This method will return a list of transactions
    """
    try:
        return jsonify(manage_transaction.get_all_transaction()), 200
    except GetTransactionsError:
        abort(404, description="There is no transactions at all")

@app.route("/insert/customers", methods=["POST"])
def insert_customers():
    """
    request = []

    This method will insert all the customers
    """
    try:
        data = request.get_json()
        manage_customers.insert_customers(data)
        return "Insert Customers", 200
    except FailedToCreateCustomers:
        abort(500, description="Failed to create customers")

@app.route("/get/customers", methods=["GET"])
def get_customers():
    """
    This method will return all thr customers
    """
    try:
        return jsonify(manage_customers.get_customers())
    except GetCustomersError:
        abort(404, "Can't find customers")

app.run(host="0.0.0.0", debug=True)