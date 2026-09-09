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
    "/transactions/<account_id> to GET transaction history for a specific account"

# Define a route for the deposit URL ("/")
@app.route("/deposit", methods = ['POST'])
def deposit():

    # get data from request
    data = request.get_json()
    # extract account_id and amount from data
    account_id = data['account_id']
    amount = data['amount']

    
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

        # create new deposit
        new_deposit= {
            "account_id": account_id,
            "amount": data["amount"],
        }

        # return sucessful deposit info
        return jsonify(new_deposit), 201

    # Handle any database errors
    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error= {"error": "Database error"}
        return jsonify(error), 500

     
# Define a route for the withdrawal URL ("/")

@app.route('/withdrawal', methods = ['POST'])
def withdrawal():
     

    # get data from request
    data = request.get_json()
    # extract account_id and amount from data
    account_id = data['account_id']
    amount = data['amount']

    try:
        # Retrieving db and cursor from function
        db, cursor =  get_db_connection()

        cursor.execute("""SELECT 
                       sum(CASE
                            WHEN transaction_type = 'deposit' THEN amount
                            WHEN transaction_type = 'withdrawal' THEN - amount
                        END) as balance
                        FROM transactions
                        WHERE account_id = %s""", (account_id,))

                      
        balance=cursor.fetchone()
        print(balance[0])
        if balanc[0]>=amount:
            cursor.execute("""INSERT INTO transactions 
                    (account_id, amount, transaction_type, transaction_date) 
                    VALUES 
                    (%s, %s, %s, %s)""", (account_id, amount, 'withdrawal', date.today()))
            # Commit changes to db
            db.commit()
            # create new deposit
            new_withdrawal= {
                    "account_id": account_id,
                    "amount": data["amount"],}
            
                # return sucessful deposit info
            return jsonify(new_withdrawal), 201
        else:
            error= {"error": "Insufficient funds"}
            return jsonify(error), 400


    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error= {"error": "Database error"}
        return jsonify(error), 500





# @app.route('/transactions/<account_id>', methods = ['GET'])
# def transactions():
#     return 

# run Flask apploication
if __name__ == "__main__":
    app.run(debug=True, port = 5000)