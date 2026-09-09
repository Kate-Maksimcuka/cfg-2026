# Investment Account Funding API

## What this project does

This project is a simple Flask API for an investment app.

A customer can:
- deposit money into their investment account
- withdraw money from their investment account
- view all transactions for a specific account

The deposits and withdrawals are saved in a MySQL database.

## Database

The database is called `Investments`.

It has one table called `transactions`.

The table has following columns:

| Column | What it stores |
|---|---|
| `transaction_id` | A unique ID for each transaction |
| `account_id` | The ID of the investment account |
| `amount` | The amount of money |
| `transaction_type` | Either `deposit` or `withdrawal` |
| `transaction_date` | The date of the transaction |

The account balance is later worked out from the transactions. Deposits are added and withdrawals are subtracted.

## API Endpoints

There are three endpoints in the API.

### 1. Deposit

**POST** `/deposit`

This adds a deposit to an account.

Example JSON:

```json
{
    "account_id": 101,
    "amount": 500
}
```

A successful deposit returns `201 Created`.

### 2. Withdrawal

**POST** `/withdrawal`

This adds a withdrawal to an account.

Before adding the withdrawal, the API checks the account balance to make sure there is enough money.

Example JSON:

```json
{
    "account_id": 101,
    "amount": 200
}
```

If there is not enough money, the API returns a `400` error.


### 3. View transactions

**GET** `/transactions/<account_id>`

This shows all transactions for a particular account.

For example:

```text
http://localhost:5000/transactions/101
```

No JSON body is needed for this request.

## Testing with Bruno

The API was tested using Bruno. You can use above example to test it.


## Project files

### `config.py`

This contains the information needed to connect to the MySQL database, such as the host, port, username, password and database name.

The password needs to be changed to your own MySQL password before running the project.

### `db_utils.py`

This contains the function that connects to MySQL.

It creates the database connection and cursor to run SQL queries.

It also has exception handling for database connection errors.

### `investment_acc.sql`

This contains the SQL used to create the `Investments` database and the `transactions` table.

It also contains the sample transaction data.

### `main.py`

This is where the Flask app and the three API endpoints are.

It handles:
- adding deposits
- checking the balance before making a withdrawal
- adding withdrawals
- showing the transaction history
- handling database errors
- closing the database connection after each request

## Database setup

Before running the project, open `config.py` and add your own MySQL password.

You may also need to change the MySQL port depending on how MySQL is set up on your computer.

For this project, I am running MySQL through Docker and using port `3307`. I use Docker because I have different development environments on my computer and had port conflicts between them.

If your MySQL uses the normal port, you can change the port in `config.py` to match your setup.

## How to run the project

1. Make sure MySQL is running.
2. Run the SQL in `investment_acc.sql` to create the database, table and sample data.
3. Open `config.py` and add your own MySQL password.
4. Install the required Python packages, including Flask, jsonify, requests, MySQL Connector, date from datetime.
5. Run the Flask app:

```bash
python main.py
```

The API will run at:

```text
http://localhost:5000
```

You can then use Bruno to test the three endpoints.

## Expected results

- A deposit is added to the database.
- A withdrawal is only added if there is enough money in the account.
- A withdrawal with insufficient funds returns an error.
- The transaction endpoint shows the transactions for the requested account.
