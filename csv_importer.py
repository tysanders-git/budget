"""
CSV Import module for the Family Budget Tracker
Handles importing transactions from CSV files
"""

import csv
import io
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from models import Transaction, Category


class CSVImporter:
    """Handles CSV file imports"""
    
    def __init__(self):
        self.categories = {cat['name'].lower(): cat['id'] 
                          for cat in Category.get_all()}
    
    def parse_csv(self, file_content: bytes, encoding: str = 'utf-8') -> List[Dict]:
        """
        Parse CSV file and return list of transaction dictionaries
        
        Expected CSV format (flexible):
        - date, description, amount, category (optional), type (optional)
        - Supports various date formats
        - Amount can be positive or negative
        """
        try:
            # Try to decode and read CSV
            content = file_content.decode(encoding)
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                content = file_content.decode('latin-1')
            except:
                content = file_content.decode('utf-8', errors='ignore')
        
        # Use pandas for flexible CSV parsing
        try:
            df = pd.read_csv(io.StringIO(content))
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
        
        transactions = []
        
        # Normalize column names (case-insensitive, strip whitespace)
        df.columns = df.columns.str.strip().str.lower()
        
        # Required columns
        required_cols = ['date', 'description', 'amount']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        for idx, row in df.iterrows():
            try:
                # Parse date (try multiple formats)
                date_str = str(row['date']).strip()
                transaction_date = self._parse_date(date_str)
                
                # Parse amount
                amount = float(str(row['amount']).replace(',', '').replace('$', '').strip())
                
                # Determine transaction type
                transaction_type = 'expense'
                if 'type' in df.columns:
                    type_str = str(row['type']).strip().lower()
                    if 'income' in type_str or 'credit' in type_str:
                        transaction_type = 'income'
                elif amount < 0:
                    transaction_type = 'income'
                    amount = abs(amount)
                elif amount > 0:
                    transaction_type = 'expense'
                
                # Get description
                description = str(row['description']).strip()
                
                # Get category
                category_id = None
                if 'category' in df.columns:
                    category_name = str(row['category']).strip()
                    category_id = self._find_category(category_name)
                
                # Get account name if available
                account_name = ""
                if 'account' in df.columns:
                    account_name = str(row['account']).strip()
                
                # Get notes if available
                notes = ""
                if 'notes' in df.columns:
                    notes = str(row['notes']).strip()
                
                transactions.append({
                    'date': transaction_date,
                    'description': description,
                    'amount': amount,
                    'category_id': category_id,
                    'transaction_type': transaction_type,
                    'account_name': account_name,
                    'notes': notes
                })
                
            except Exception as e:
                # Skip rows that can't be parsed
                print(f"Warning: Skipping row {idx + 1}: {str(e)}")
                continue
        
        return transactions
    
    def _parse_date(self, date_str: str) -> datetime.date:
        """Parse date string in various formats"""
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y.%m.%d',
            '%d.%m.%Y',
            '%m.%d.%Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _find_category(self, category_name: str) -> Optional[int]:
        """Find category ID by name (case-insensitive, fuzzy matching)"""
        if not category_name:
            return None
        
        category_lower = category_name.lower().strip()
        
        # Exact match
        if category_lower in self.categories:
            return self.categories[category_lower]
        
        # Partial match
        for cat_name, cat_id in self.categories.items():
            if category_lower in cat_name or cat_name in category_lower:
                return cat_id
        
        return None
    
    def import_transactions(self, file_content: bytes, 
                           preview: bool = False) -> Dict:
        """
        Import transactions from CSV file
        
        Returns:
            Dict with 'success', 'imported', 'skipped', 'errors' keys
        """
        try:
            transactions = self.parse_csv(file_content)
            
            if preview:
                return {
                    'success': True,
                    'preview': transactions,
                    'count': len(transactions)
                }
            
            imported = 0
            skipped = 0
            errors = []
            
            for trans in transactions:
                try:
                    Transaction.create(**trans)
                    imported += 1
                except Exception as e:
                    skipped += 1
                    errors.append(f"Error importing {trans.get('description', 'transaction')}: {str(e)}")
            
            return {
                'success': True,
                'imported': imported,
                'skipped': skipped,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'imported': 0,
                'skipped': 0,
                'errors': []
            }

