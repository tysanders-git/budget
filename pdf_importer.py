"""
PDF Import module for the Family Budget Tracker
Handles importing transactions from PDF bank statements
"""

import re
import io
from datetime import datetime
from typing import List, Dict, Optional
import pdfplumber
from models import Transaction, Category


class PDFImporter:
    """Handles PDF bank statement imports"""
    
    def __init__(self):
        self.categories = {cat['name'].lower(): cat['id'] 
                          for cat in Category.get_all()}
    
    def extract_text(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            # Use pdfplumber (better for tables)
            pdf_file = io.BytesIO(file_content)
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def extract_table_data(self, file_content: bytes) -> List[Dict]:
        """Extract table data from PDF (for structured statements)"""
        transactions = []
        try:
            pdf_file = io.BytesIO(file_content)
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if table and len(table) > 1:  # Has header and data
                            # Try to identify transaction rows
                            for row in table[1:]:  # Skip header
                                if row and len(row) >= 3:
                                    trans = self._parse_table_row(row)
                                    if trans:
                                        transactions.append(trans)
        except Exception:
            pass  # If table extraction fails, fall back to text parsing
        
        return transactions
    
    def _parse_table_row(self, row: List) -> Optional[Dict]:
        """Parse a table row into a transaction"""
        try:
            # Common patterns: Date, Description, Amount
            if len(row) < 3:
                return None
            
            # Find date
            date_str = None
            amount_str = None
            description = ""
            
            for cell in row:
                if cell:
                    cell_str = str(cell).strip()
                    # Check if it's a date
                    if self._looks_like_date(cell_str) and not date_str:
                        date_str = cell_str
                    # Check if it's an amount
                    elif self._looks_like_amount(cell_str) and not amount_str:
                        amount_str = cell_str
                    # Otherwise it's likely description
                    elif cell_str and not date_str and not amount_str:
                        description += " " + cell_str
            
            if date_str and amount_str:
                transaction_date = self._parse_date(date_str)
                amount = self._parse_amount(amount_str)
                transaction_type = 'expense' if amount > 0 else 'income'
                amount = abs(amount)
                
                return {
                    'date': transaction_date,
                    'description': description.strip(),
                    'amount': amount,
                    'category_id': None,
                    'transaction_type': transaction_type,
                    'account_name': '',
                    'notes': ''
                }
        except Exception:
            pass
        
        return None
    
    def parse_pdf(self, file_content: bytes) -> List[Dict]:
        """Parse PDF and extract transactions"""
        transactions = []
        
        # Try table extraction first
        table_transactions = self.extract_table_data(file_content)
        if table_transactions:
            return table_transactions
        
        # Fall back to text parsing
        text = self.extract_text(file_content)
        
        # Common patterns for bank statements
        lines = text.split('\n')
        current_date = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract date
            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', line)
            if date_match:
                try:
                    current_date = self._parse_date(date_match.group(1))
                except:
                    pass
            
            # Try to extract amount
            amount_match = re.search(r'[\$]?([\d,]+\.?\d*)', line)
            if amount_match and current_date:
                try:
                    amount_str = amount_match.group(1).replace(',', '')
                    amount = float(amount_str)
                    
                    # Extract description (everything except date and amount)
                    description = line
                    if date_match:
                        description = description.replace(date_match.group(0), '').strip()
                    description = re.sub(r'[\$]?[\d,]+\.?\d*', '', description).strip()
                    
                    if description and amount > 0:
                        transaction_type = 'expense'
                        # Check for credit indicators
                        if any(word in description.lower() for word in ['credit', 'deposit', 'refund']):
                            transaction_type = 'income'
                        
                        transactions.append({
                            'date': current_date,
                            'description': description,
                            'amount': abs(amount),
                            'category_id': None,
                            'transaction_type': transaction_type,
                            'account_name': '',
                            'notes': ''
                        })
                except:
                    pass
        
        return transactions
    
    def _looks_like_date(self, text: str) -> bool:
        """Check if text looks like a date"""
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
            r'\d{1,2}\.\d{1,2}\.\d{2,4}',
            r'\d{1,2}\s+\w{3}\s+\d{4}'
        ]
        return any(re.search(pattern, text) for pattern in date_patterns)
    
    def _looks_like_amount(self, text: str) -> bool:
        """Check if text looks like an amount"""
        amount_patterns = [
            r'[\$]?[\d,]+\.?\d{2}',
            r'[\d,]+\.\d{2}'
        ]
        return any(re.search(pattern, text) for pattern in amount_patterns)
    
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
            '%m.%d.%Y',
            '%d %b %Y',
            '%d %B %Y'
        ]
        
        # Clean date string
        date_str = date_str.strip()
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string"""
        # Remove currency symbols and commas
        cleaned = amount_str.replace('$', '').replace(',', '').strip()
        # Handle negative amounts
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        return float(cleaned)
    
    def _find_category(self, description: str) -> Optional[int]:
        """Try to auto-categorize based on description"""
        description_lower = description.lower()
        
        # Simple keyword matching
        category_keywords = {
            'groceries': ['grocery', 'supermarket', 'food', 'walmart', 'target'],
            'transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'parking'],
            'entertainment': ['netflix', 'spotify', 'movie', 'cinema', 'game'],
            'bills & utilities': ['electric', 'water', 'internet', 'phone', 'utility'],
            'healthcare': ['pharmacy', 'doctor', 'medical', 'hospital', 'clinic'],
            'shopping': ['amazon', 'store', 'shop', 'mall']
        }
        
        for category_name, keywords in category_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                cat_id = self.categories.get(category_name.lower())
                if cat_id:
                    return cat_id
        
        return None
    
    def import_transactions(self, file_content: bytes, 
                           preview: bool = False) -> Dict:
        """
        Import transactions from PDF file
        
        Returns:
            Dict with 'success', 'imported', 'skipped', 'errors' keys
        """
        try:
            transactions = self.parse_pdf(file_content)
            
            # Try to auto-categorize
            for trans in transactions:
                if not trans.get('category_id'):
                    trans['category_id'] = self._find_category(trans['description'])
            
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
