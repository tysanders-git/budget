"""
Database module for the Family Budget Tracker
Handles SQLite database initialization and connection
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional


class Database:
    """Manages database connection and initialization"""
    
    def __init__(self, db_path: str = "budget_tracker.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database and tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        # Ensure immediate writes to disk
        self.conn.execute("PRAGMA synchronous = NORMAL")
        self.conn.execute("PRAGMA journal_mode = WAL")
        cursor = self.conn.cursor()
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Budgets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id),
                UNIQUE(category_id, year, month)
            )
        """)
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
                account_name TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        # Goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                target_date DATE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Recurring transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recurring_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
                frequency TEXT NOT NULL CHECK(frequency IN ('daily', 'weekly', 'monthly', 'yearly')),
                start_date DATE NOT NULL,
                end_date DATE,
                next_due_date DATE,
                account_name TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_budgets_year_month ON budgets(year, month)")
        
        # Insert default categories if they don't exist
        default_categories = [
            ('Housing', 'Rent, mortgage, utilities'),
            ('Food & Groceries', 'Groceries, dining out'),
            ('Transportation', 'Gas, car maintenance, public transport'),
            ('Healthcare', 'Medical expenses, insurance'),
            ('Entertainment', 'Movies, hobbies, subscriptions'),
            ('Education', 'School fees, books, courses'),
            ('Shopping', 'Clothing, household items'),
            ('Bills & Utilities', 'Phone, internet, electricity'),
            ('Personal Care', 'Haircuts, toiletries'),
            ('Savings', 'Savings contributions'),
            ('Income', 'Salary, freelance, other income'),
            ('Other', 'Miscellaneous expenses')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                default_categories
            )
        
        self.conn.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            # Ensure immediate writes to disk
            self.conn.execute("PRAGMA synchronous = NORMAL")
            self.conn.execute("PRAGMA journal_mode = WAL")
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Global database instance
db = Database()

