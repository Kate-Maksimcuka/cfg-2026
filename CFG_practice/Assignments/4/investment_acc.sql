--Database schema

CREATE DATABASE Investments;

USE Investments;

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    amount DECIMAL(19, 4) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    transaction_date DATE NOT NULL,
    CONSTRAINT chk_transaction_type CHECK (transaction_type IN ('deposit', 'withdrawal'))
);

-- Insert data
INSERT INTO transactions (account_id, amount, transaction_type, transaction_date)
VALUES
    (101, 1000.0000, 'deposit',    '2026-01-05'),
    (101, 250.0000,  'withdrawal', '2026-01-12'),
    (101, 500.0000,  'deposit',    '2026-02-03'),
    (101, 100.0000,  'withdrawal', '2026-02-15'),
    (101, 750.0000,  'deposit',    '2026-03-01'),

    (102, 2000.0000, 'deposit',    '2026-01-10'),
    (102, 500.0000,  'withdrawal', '2026-01-20'),
    (102, 300.0000,  'deposit',    '2026-02-08'),
    (102, 150.0000,  'withdrawal', '2026-02-22'),
    (102, 1000.0000, 'deposit',    '2026-03-05'),

    (103, 500.0000,  'deposit',    '2026-01-15'),
    (103, 100.0000,  'withdrawal', '2026-01-25'),
    (103, 750.0000,  'deposit',    '2026-02-10'),
    (103, 200.0000,  'withdrawal', '2026-02-18'),
    (103, 250.0000,  'deposit',    '2026-03-03'),

    (104, 5000.0000, 'deposit',    '2026-01-07'),
    (104, 1200.0000, 'withdrawal', '2026-01-30'),
    (104, 800.0000,  'deposit',    '2026-02-14'),
    (104, 300.0000,  'withdrawal', '2026-02-28'),
    (104, 1500.0000, 'deposit',    '2026-03-10');