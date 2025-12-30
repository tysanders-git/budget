"""
Reports and visualization module for the Family Budget Tracker
Generates charts and reports for spending analysis
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models import Transaction, Budget


class Reports:
    """Generate reports and visualizations"""
    
    @staticmethod
    def get_monthly_summary(year: int, month: int) -> Dict:
        """Get monthly spending summary"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        transactions = Transaction.get_all(start_date=start_date, end_date=end_date)
        
        total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
        net_balance = total_income - total_expenses
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'transaction_count': len(transactions)
        }
    
    @staticmethod
    def get_category_spending_chart(start_date: date, end_date: date, transaction_type: str = 'expense') -> go.Figure:
        """Create pie chart of spending by category"""
        summary = Transaction.get_summary_by_category(start_date, end_date, transaction_type)
        
        if not summary:
            # Return empty chart
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig
        
        df = pd.DataFrame(summary)
        
        title = 'Income by Category' if transaction_type == 'income' else 'Spending by Category'
        
        fig = px.pie(
            df, 
            values='total_amount', 
            names='category_name',
            title=title,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def get_spending_trend_chart(start_date: date, end_date: date) -> go.Figure:
        """Create line chart showing spending trends over time"""
        transactions = Transaction.get_all(start_date=start_date, end_date=end_date)
        
        if not transactions:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by date and transaction type
        daily_summary = df.groupby([df['date'].dt.date, 'transaction_type'])['amount'].sum().reset_index()
        daily_summary['date'] = pd.to_datetime(daily_summary['date'])
        
        fig = go.Figure()
        
        for trans_type in ['income', 'expense']:
            type_data = daily_summary[daily_summary['transaction_type'] == trans_type]
            fig.add_trace(go.Scatter(
                x=type_data['date'],
                y=type_data['amount'],
                mode='lines+markers',
                name=trans_type.title(),
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title='Spending Trends Over Time',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def get_budget_vs_actual_chart(year: int, month: int) -> go.Figure:
        """Create bar chart comparing budget vs actual spending"""
        budget_data = Budget.get_budget_vs_actual(year, month)
        
        if not budget_data:
            fig = go.Figure()
            fig.add_annotation(text="No budget data available", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig
        
        df = pd.DataFrame(budget_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Budgeted',
            x=df['category_name'],
            y=df['budgeted_amount'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Actual',
            x=df['category_name'],
            y=df['actual_amount'],
            marker_color='coral'
        ))
        
        fig.update_layout(
            title='Budget vs Actual Spending',
            xaxis_title='Category',
            yaxis_title='Amount ($)',
            barmode='group',
            xaxis_tickangle=-45
        )
        
        return fig
    
    @staticmethod
    def get_category_comparison_chart(start_date: date, end_date: date) -> go.Figure:
        """Create bar chart comparing categories"""
        summary = Transaction.get_summary_by_category(start_date, end_date, 'expense')
        
        if not summary:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5)
            return fig
        
        df = pd.DataFrame(summary)
        df = df.sort_values('total_amount', ascending=True)
        
        fig = px.bar(
            df,
            x='total_amount',
            y='category_name',
            orientation='h',
            title='Spending by Category',
            labels={'total_amount': 'Amount ($)', 'category_name': 'Category'}
        )
        
        return fig
    
    @staticmethod
    def get_monthly_comparison(start_year: int, start_month: int, 
                               num_months: int = 6) -> go.Figure:
        """Compare spending across multiple months"""
        months_data = []
        
        current_year = start_year
        current_month = start_month
        
        for _ in range(num_months):
            start_date = date(current_year, current_month, 1)
            if current_month == 12:
                end_date = date(current_year + 1, 1, 1)
                current_year += 1
                current_month = 1
            else:
                end_date = date(current_year, current_month + 1, 1)
                current_month += 1
            
            transactions = Transaction.get_all(start_date=start_date, end_date=end_date)
            total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
            
            months_data.append({
                'month': f"{start_date.strftime('%Y-%m')}",
                'total_expenses': total_expenses
            })
        
        df = pd.DataFrame(months_data)
        
        fig = px.bar(
            df,
            x='month',
            y='total_expenses',
            title='Monthly Spending Comparison',
            labels={'month': 'Month', 'total_expenses': 'Total Expenses ($)'}
        )
        
        return fig
    
    @staticmethod
    def export_to_csv(start_date: date, end_date: date, 
                      output_path: str = "transactions_export.csv"):
        """Export transactions to CSV"""
        transactions = Transaction.get_all(start_date=start_date, end_date=end_date)
        df = pd.DataFrame(transactions)
        
        # Select relevant columns
        export_df = df[['date', 'description', 'amount', 'category_name', 
                       'transaction_type', 'account_name', 'notes']]
        
        export_df.to_csv(output_path, index=False)
        return output_path

