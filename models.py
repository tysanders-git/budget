"""
Data models for the Family Budget Tracker
Provides helper functions for database operations
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from db import db


class Category:
    """Category model"""
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all categories"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict]:
        """Get category by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def create(name: str, description: str = "") -> int:
        """Create a new category"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def delete(category_id: int) -> bool:
        """Delete a category"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return cursor.rowcount > 0


class Transaction:
    """Transaction model"""
    
    @staticmethod
    def create(date: date, description: str, amount: float, 
               category_id: Optional[int], transaction_type: str,
               account_name: str = "", notes: str = "") -> int:
        """Create a new transaction"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions 
            (date, description, amount, category_id, transaction_type, account_name, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date, description, amount, category_id, transaction_type, 
              account_name, notes))
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def get_all(start_date: Optional[date] = None, 
                end_date: Optional[date] = None,
                category_id: Optional[int] = None) -> List[Dict]:
        """Get all transactions with optional filters"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT t.*, c.name as category_name 
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND t.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND t.date <= ?"
            params.append(end_date)
        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)
        
        query += " ORDER BY t.date DESC, t.id DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict]:
        """Get transaction by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.*, c.name as category_name 
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
        """, (transaction_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def update(transaction_id: int, date: date, description: str, 
               amount: float, category_id: Optional[int], 
               transaction_type: str, account_name: str = "", 
               notes: str = "") -> bool:
        """Update a transaction"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions 
            SET date = ?, description = ?, amount = ?, category_id = ?,
                transaction_type = ?, account_name = ?, notes = ?
            WHERE id = ?
        """, (date, description, amount, category_id, transaction_type,
              account_name, notes, transaction_id))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(transaction_id: int) -> bool:
        """Delete a transaction"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def get_summary_by_category(start_date: date, end_date: date, 
                                transaction_type: str = 'expense') -> List[Dict]:
        """Get spending summary by category"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.name as category_name,
                c.id as category_id,
                COALESCE(SUM(t.amount), 0) as total_amount,
                COUNT(t.id) as transaction_count
            FROM categories c
            LEFT JOIN transactions t ON c.id = t.category_id 
                AND t.date >= ? AND t.date <= ? 
                AND t.transaction_type = ?
            GROUP BY c.id, c.name
            HAVING total_amount > 0
            ORDER BY total_amount DESC
        """, (start_date, end_date, transaction_type))
        return [dict(row) for row in cursor.fetchall()]


class Budget:
    """Budget model"""
    
    @staticmethod
    def create(category_id: int, year: int, month: int, amount: float) -> int:
        """Create or update a budget"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (category_id, year, month, amount)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(category_id, year, month) 
            DO UPDATE SET amount = excluded.amount
        """, (category_id, year, month, amount))
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def get_by_month(year: int, month: int) -> List[Dict]:
        """Get all budgets for a specific month"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE b.year = ? AND b.month = ?
            ORDER BY c.name
        """, (year, month))
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_budget_vs_actual(year: int, month: int) -> List[Dict]:
        """Get budget vs actual spending comparison"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get start and end dates for the month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        cursor.execute("""
            SELECT 
                b.id as budget_id,
                c.id as category_id,
                c.name as category_name,
                b.amount as budgeted_amount,
                COALESCE(SUM(t.amount), 0) as actual_amount,
                (b.amount - COALESCE(SUM(t.amount), 0)) as difference,
                CASE 
                    WHEN b.amount > 0 THEN 
                        (COALESCE(SUM(t.amount), 0) / b.amount * 100)
                    ELSE 0
                END as percentage_used
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            LEFT JOIN transactions t ON c.id = t.category_id 
                AND t.date >= ? AND t.date < ? 
                AND t.transaction_type = 'expense'
            WHERE b.year = ? AND b.month = ?
            GROUP BY b.id, c.id, c.name, b.amount
            ORDER BY c.name
        """, (start_date, end_date, year, month))
        return [dict(row) for row in cursor.fetchall()]


class Goal:
    """Financial goal model"""
    
    @staticmethod
    def create(name: str, target_amount: float, target_date: Optional[date] = None,
               description: str = "") -> int:
        """Create a new financial goal"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO goals (name, target_amount, target_date, description)
            VALUES (?, ?, ?, ?)
        """, (name, target_amount, target_date, description))
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all goals"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals ORDER BY target_date, name")
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_progress(goal_id: int, current_amount: float) -> bool:
        """Update goal progress"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE goals SET current_amount = ? WHERE id = ?
        """, (current_amount, goal_id))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(goal_id: int) -> bool:
        """Delete a goal"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()
        return cursor.rowcount > 0

