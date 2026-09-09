# Imports
from db_utils import get_db_connection
import mysql.connector
from flask import Flask, request, jsonify
from datetime import date


# Create a new Flask app instance
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route("/")
def hello_client():
    # Return a welcome message and list available endpoints
    return "Welcome to the Investment Account Funding API. <br>" \
    "Available endpoints: <br>" \
    "/deposit to POST deposits <br>" \
    "/withdrawal to POST withdrawals <br>" \
    "/transactions/account_id to GET transaction history for a specific account"

# Define a route for the deposit URL ("/deposit")
@app.route("/deposit", methods = ['POST'])

# Define a function to handle deposit requests
def deposit():

    # Get data from request
    data = request.get_json()
    # extract account_id and amount from data
    account_id = data['account_id']
    amount = data['amount']

    # Try to connect to the database and deposit transaction
    try:
        # Retrieving db and cursor from function
        db, cursor =  get_db_connection()

        # Execute cursor to innsert data into transactions
        cursor.execute(
        """INSERT INTO transactions 
        (account_id, amount, transaction_type, transaction_date) 
        VALUES 
        (%s, %s, %s, %s)""", (account_id, amount, 'deposit', date.today()))

        # Commit changes to db
        db.commit()

        # Create new deposit
        new_deposit = {
            "account_id": account_id,
            "amount": data["amount"],}

        # Return sucessful deposit info
        return jsonify(new_deposit), 201

    # Handle any database errors
    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error = {"error": "Database error"}
        return jsonify(error), 500
    
    # Close the database connection
    finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

# Define a route for the withdrawal URL ("/withdrawal")
@app.route('/withdrawal', methods = ['POST'])

# Define a function to handle withdrawal requests
def withdrawal():
     
    # Get data from request
    data = request.get_json()

    # Extract account_id and amount from data
    account_id = data['account_id']
    amount = data['amount']

    # Try to connect to the database and withdraw transaction
    try:
        # Retrieving db and cursor from function
        db, cursor =  get_db_connection()

        # Execute cursor to calculate the current balance for the given account_id
        cursor.execute("""SELECT 
                       sum(CASE
                            WHEN transaction_type = 'deposit' THEN amount
                            WHEN transaction_type = 'withdrawal' THEN - amount
                        END) as balance
                        FROM transactions
                        WHERE account_id = %s""", (account_id,))

        # Fetch the balance from the cursor          
        balance = cursor.fetchone()
        print(balance[0])

        # Check if the balance is sufficient for the withdrawal then insert withdrawal transaction
        if balance[0] >= amount:
            cursor.execute("""INSERT INTO transactions 
                    (account_id, amount, transaction_type, transaction_date) 
                    VALUES 
                    (%s, %s, %s, %s)""", (account_id, amount, 'withdrawal', date.today()))
            
            # Commit changes to db
            db.commit()

            # Create new withdrawal
            new_withdrawal = {
                    "account_id": account_id,
                    "amount": data["amount"]}
            
            # Confirm sucessful withdrawal info or error
            return jsonify(new_withdrawal), 201
        else:
            error = {"error": "Insufficient funds"}
            return jsonify(error), 400

    # Handle any database errors
    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error = {"error": "Database error"}
        return jsonify(error), 500
    
    # Close the database connection
    finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

# Define a route for the transactions URL ("/transactions/<account_id>")
@app.route('/transactions/<account_id>', methods = ['GET'])

# Define a function to retrieve transactions for a specific account_id
def transactions(account_id):
    try:
        # Retrieving db and cursor from function
        db, cursor =  get_db_connection()

        # Execute cursor to select transactions for the given account_id
        cursor.execute("""SELECT * FROM transactions WHERE account_id = %s""", (account_id,))
        transactions = cursor.fetchall()

        # Checks if any transactions were found for the given account_id
        if not transactions:
            return jsonify({"error": f"Account_id not found with id {account_id}"}), 404

        # Create a list of transaction dictionaries
        transaction_list = []

        # Loop through the transactions and create a dictionary for each transaction
        for transaction in transactions:
            transaction_dict = {
                "transaction_id": transaction[0],
                "account_id": transaction[1],
                "amount": float(transaction[2]),
                "transaction_type": transaction[3],
                "transaction_date": transaction[4]}

            # Append the transaction dictionary to the list
            transaction_list.append(transaction_dict)

        # Return the list of transactions
        return jsonify(transaction_list), 200

    # Handle any database errors
    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error = {"error": "Database error"}
        return jsonify(error), 500
    
    # Close the database connection
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

# run Flask application
if __name__ == "__main__":
    app.run(debug=True, port = 5000)