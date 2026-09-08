# Imports
from db_utils import get_db_connection
import mysql.connector
from flask import Flask, request, jsonify
from datetime import date


# Create a new Flask app instance
app = Flask(__name__)

# Define a route for the deposit URL ("/")
@app.route("/deposit", methods = ['POST'])
def deposit():

    # get data from request
    data = request.get_json()
    account_id = data['account_id']
    amount = data['amount']
    try:
        # Retrieving db and cursor from function
        db, cursor =  get_db_connection()
        cursor.execute(
        """INSERT INTO transactions 
        (account_id, amount, transaction_type, transaction_date) 
        VALUES 
        (%s, %s, %s, %s)""", (account_id, amount, 'deposit', date.today())
        )
        db.commit()

        # create new deposit
        new_deposit= {
            "account_id": account_id,
            "amount": data["amount"],
        }

        return jsonify(new_deposit), 201

    
    except mysql.connector.Error as err:
        print(f"Something has gone wrong: {err}")
        error= {
                    "error": "Database error"
                }
        return jsonify(error), 500

     

# @app.route('/withdrawal', methods = ['POST'])
# def withdrawal():
#     return 

# @app.route('/transactions/<account_id>', methods = ['GET'])
# def transactions():
#     return 

# run Flask apploication
if __name__ == "__main__":
    app.run(debug=True, port = 5000)