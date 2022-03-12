from datetime import datetime
from locale import currency
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools.error_handling import FailedToCreateCustomers
from tools.error_handling import TransactionFailedError, CustomerNotFoundError
from tools.error_handling import DeleteTransactionFailedError,GetTransactionsError
from tools.error_handling import GetCustomersError, TransactionNotFoundError
from tools.error_handling import UpdateTransactionFailed
from tools.base import Base
from tools.customer_table import Customer
from tools.transaction_table import Transaction


class SqlDB:
    def __init__(self,  user:str, 
                        password:str, 
                        host:str, 
                        db:str, 
                        type:str,
                        logger:object):
        """
        Args:
        -----
            user(str): The user name of the db user
            password(str): The password of the db user
            host(str): The host of the db
            db(str): The database that it will connect
            type(str): The kind of the db -> mysql
            logger(Logger): The object of the logger controller
        """
        try:
            self.logger = logger
            self.engine = create_engine(f"{type}://{user}:{password}@{host}/{db}", 
                                    echo=True)
            Base.metadata.create_all(self.engine)
            self.session = sessionmaker(bind=self.engine)
            self.logger.log.debug(f"connect to SQL DB {type}")
        except Exception:
            self.logger.log.critical(
                f"could not connect to SQL DB {type}", exc_info=True)
            sys.exit()
    def create_transaction(self, 
                            client_id_send:str, 
                            client_id_get:str, 
                            client_send_total:float, 
                            client_get_total:float,
                            total_before_convert:float,
                            currency_user_send:str,
                            total_after_convert:float,
                            currency_user_get:str):
        """
        This method will create new transaction and it will update
        the total of the two customers.

        Args:
        -----
            client_id_send(str): The id of the customer who do the transaction
            client_id_get(str): The id of the customer who get the money
            client_send_total(float): The total money of the customer sender 
                                      after transaction
            client_get_total(float): The total money of the customer who get the money
                                        after transaction
            total_before_convert(float): The money which the sender send in is own
                                         currency 
            currency_user_send(str): The currency of the sender
            total_after_convert(float): The money after convertion into the
                                        getter currency
            currency_user_get(str): The currency of the getter
        """
        try:
            with self.session() as session:
                with session.begin():
                    trans = Transaction(user_id_transac=client_id_send,
                                        user_id_get=client_id_get,
                                        total_before_convert=total_before_convert,
                                        currency_user_transac=currency_user_send,
                                        total_after_convert=total_after_convert,
                                        currency_user_get=currency_user_get,
                                        date=datetime.now())
                    self.update_costumer_total_session(client_id_send,client_send_total,session)
                    self.update_costumer_total_session(client_id_get, client_get_total, session)
                    session.add(trans)
                    session.commit()                  
        except Exception:
            self.logger.log.error("Failed to create transaction:",exc_info=True)
            
            raise TransactionFailedError(f"client sender: {client_id_send} \
                                            can't do transaction to client: \
                                            {client_id_get}")
        
    
    def update_transaction(self,
                            client_id_send:str, 
                            client_id_get:str, 
                            client_send_total:float, 
                            client_get_total:float,
                            transaction_id:int,
                            total_before_convert:float,
                            currency_user_send:str,
                            total_after_convert:float,
                            currency_user_get:str):
        """
        This method will update a transaction. 

         Args:
        -----
            client_id_send(str): The id of the customer who do the transaction
            client_id_get(str): The id of the customer who get the money
            client_send_total(float): The total money of the customer sender 
                                      after transaction
            client_get_total(float): The total money of the customer who get the money
                                        after transaction
            transaction_id(int): The primary key of the transaction
            total_before_convert(float): The money which the sender send in is own
                                         currency 
            currency_user_send(str): The currency of the sender
            total_after_convert(float): The money after convertion into the
                                        getter currency
            currency_user_get(str): The currency of the getter
        """
        try:
            with self.session() as session:
                with session.begin():
                        self.update_transaction_session(session,
                                                        transaction_id, 
                                                        client_id_send, 
                                                        client_id_get, 
                                                        total_before_convert, 
                                                        currency_user_send, 
                                                        total_after_convert, 
                                                        currency_user_get)
                        
                        self.update_costumer_total_session( client_id_send,
                                                            client_send_total,
                                                            session)
                        
                        self.update_costumer_total_session( client_id_get, 
                                                            client_get_total, 
                                                            session)
                        session.commit()
        except Exception:
            self.logger.log.error("Failed to update",exc_info=True)
            raise UpdateTransactionFailed(f"Failed to update transaction")
        
    
    def update_transaction_session( self,
                                    session:object, 
                                    transaction_id:int, 
                                    user_id_transac:str,
                                    user_id_get:str, 
                                    total_before_convert:float, 
                                    currency_user_send:str, 
                                    total_after_convert:float, 
                                    currency_user_get:str):
        """
        This method will update a transaction object.

        Args:
        -----
            transaction_id(int): The primary key of the transaction
            total_before_convert(float): The money which the sender send 
                                         in is currency 
            currency_user_send(str): The currency of the sender
            total_after_convert(float): The money after convertion into the
                                        getter currency
            currency_user_get(str): The currency of the getter

        """
        try:
            trans = session.query(Transaction).filter(Transaction.id == transaction_id).first()

            if(trans == None):
                raise TransactionNotFoundError(f"The transaction is not found {transaction_id}")
            trans.user_id_transac = user_id_transac
            trans.user_id_get = user_id_get
            trans.total_before_convert = total_before_convert
            trans.currency_user_transac = currency_user_send
            trans.total_after_convert = total_after_convert
            trans.currency_user_get = currency_user_get
            trans.date = datetime.now()
        
        except Exception:
            self.logger.log.error("Failed to fetch",exc_info=True)
            raise TransactionNotFoundError(f"The transaction is not found {transaction_id}")

    def delete_transaction(self, 
                                transaction_id:int, 
                                client_id_send:str,
                                client_id_get:str, 
                                client_send_total:float, 
                                client_get_total:float):
        """
        This method will delete a transaction.

          Args:
        -----
            transaction_id(int): The primary key of the transaction
            client_id_send(str): The id of the customer who do the transaction
            client_id_get(str): The id of the customer who get the money
            client_send_total(float): The total money of the customer sender 
                                      before transaction
            client_get_total(float): The total money of the customer who 
                                     get the money before transaction      
        """
        try:
            with self.session() as session:
                with session.begin():
                    trans = self.get_transaction_session(transaction_id, session)
                    self.update_costumer_total_session(client_id_send,client_send_total,session)
                    self.update_costumer_total_session(client_id_get, client_get_total, session)
                    session.delete(trans)
                    session.commit()
        except Exception:
            self.logger.log.error("Failed to delete:",exc_info=True)
            raise DeleteTransactionFailedError(f"Failed to delete transaction \
                                                {transaction_id}")
        
    def get_transactions(self) -> list:
        """
        This method will return a list of transactions.

        Retrun:
        -------
            Return a list of transaction objects
        """
        try:
            trans = []
            with self.session() as session:
                trans = session.query(Transaction).all()
            return trans
        except Exception:
            self.logger.log.error("Failed to fetch",exc_info=True)
            raise GetTransactionsError(f"Failed to get Transactions")
    
    def get_transaction_session(self, transaction_id:int, session:object) -> object:
        try:
            """
            This method will return a specific transaction

            Args:
            -----
                transaction_id(int): The primary key of the transaction
                session(Session): The session object of sqlalchemy
            
            Return:
            -------
                Return an object
            """
            trans = session.query(Transaction).filter(Transaction.id == transaction_id).first()
            if(trans == None):
                raise TransactionNotFoundError(f"The transaction not found {transaction_id}")
            return trans
        except Exception:
            self.logger.log.error("Failed to fetch:",exc_info=True)
            raise TransactionNotFoundError(f"The transaction not found {transaction_id}")
   
    def update_costumer_total_session(self, 
                                            client_id:str, 
                                            total:float, 
                                            session:object):
        """
        This method will update the total_price of a customer

        Args:
        -----
            client_id(str): The customer id
            total(float): The total price of the customer
            session(Session): The session object of sqlalchemy
        """
        try:
            customer = session.query(Customer).filter(Customer.customer_id == client_id).first()
          
            if(customer == None):
                raise CustomerNotFoundError(f"Customer not found {client_id}") 

            customer.total_price = total
        except Exception:
            self.logger.log.error("Failed to fetch",exc_info=True)
            raise CustomerNotFoundError(f"Customer not found {client_id}")    
    
    
    def get_customer(self, client_id:str) -> dict:
        """
        This method will return a customer.

        Args:
        -----
            client_id(str): The customer id
        
        Retrun:
        ------
            Return the customer dict
        """
        try:
            customer = ""
            with self.session() as session:
                customer = session.query(Customer).filter(
                                Customer.customer_id == client_id).first()
            
            if(customer == None):
                raise CustomerNotFoundError(f"The customer is not found {client_id}")
            return customer.__dict__ 
        except Exception:
            self.logger.log.error("Failed to fetch:",exc_info=True)
            raise CustomerNotFoundError(f"The customer is not found {client_id}")
    
    def get_transaction(self, transaction_id:int) -> dict:
        """
        This method will return the transaction.

        Args:
        -----
            transaction_id(int): The id of the transaction

        Return:
        -------
            Return the transaction dict

        """
        try:
            trans = ""
            with self.session() as session:
                trans = session.query(Transaction).filter(Transaction.id == transaction_id).first()
            if(trans == None):
                raise TransactionNotFoundError(f"The transaction not found {transaction_id}")
            return trans.__dict__
        except Exception:
            self.logger.log.error("Failed to Fetch:",exc_info=True)
            raise TransactionNotFoundError(f"The transaction not found {transaction_id}")
    
    def get_customers(self) -> list:
        """
        This method will return all the customers

        Retrun:
        -------
            A list of customers objects
        """
        try:
            customers = []
            with self.session() as session:
                customers = session.query(Customer).all()
            return customers
        except Exception:
            self.logger.log.error("Failed to fetch:",exc_info=True)
            raise GetCustomersError(f"Can't fetch from customer table")

    def insert_customer(self,  customer_id:str,
                                first_name:str,
                                last_name:str,
                                email:str,
                                gender:str,
                                country:str,
                                city:str,
                                street:str,
                                phone:str,
                                total_price:float,
                                currency:str,
                                credit_card_type:str,
                                credit_card_number:str):
        """
        This method will create a new customer

        """
        try:
            with self.session() as session:
                with session.begin():
                    customer = session.query(Customer).filter(
                                        Customer.customer_id==customer_id).first()
                    print(customer)
                    if(customer == None):
                        session.add(Customer(
                                        customer_id=customer_id, 
                                        first_name=first_name, 
                                        last_name=last_name,
                                        email=email, 
                                        gender=gender, 
                                        country=country, 
                                        city=city, 
                                        street=street, 
                                        phone=phone, 
                                        total_price=total_price, 
                                        currency=currency,
                                        credit_card_type=credit_card_type,
                                        credit_card_number=credit_card_number
                                        ))
                        session.commit()
        except Exception:
            self.logger.log.error("Failed to insert:",exc_info=True)
            raise FailedToCreateCustomers("Failed to create customers")
                
