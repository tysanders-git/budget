"""
Main Streamlit application for Family Budget Tracker
"""

import streamlit as st
from datetime import date, datetime
import pandas as pd
from models import Transaction, Category, Budget, Goal
from csv_importer import CSVImporter
from pdf_importer import PDFImporter
from reports import Reports

# Page configuration
st.set_page_config(
    page_title="Family Budget Tracker 2026",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_year' not in st.session_state:
    st.session_state.current_year = 2026
if 'current_month' not in st.session_state:
    st.session_state.current_month = datetime.now().month


def main():
    """Main application"""
    st.title("💰 Family Budget Tracker 2026")
    
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.success("💾 Auto-Save: All data is automatically saved to SQLite database")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Transactions", "Budget Planning", "Reports", "Categories", "Goals", "Import Data"]
    )
    
    # Year and month selector in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Time Period")
    st.session_state.current_year = st.sidebar.selectbox(
        "Year",
        range(2020, 2030),
        index=st.session_state.current_year - 2020
    )
    st.session_state.current_month = st.sidebar.selectbox(
        "Month",
        range(1, 13),
        index=st.session_state.current_month - 1
    )
    
    # Route to appropriate page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Transactions":
        show_transactions()
    elif page == "Budget Planning":
        show_budget_planning()
    elif page == "Reports":
        show_reports()
    elif page == "Categories":
        show_categories()
    elif page == "Goals":
        show_goals()
    elif page == "Import Data":
        show_import_data()


def show_dashboard():
    """Display main dashboard"""
    st.header("📊 Dashboard")
    
    year = st.session_state.current_year
    month = st.session_state.current_month
    
    # Get monthly summary
    summary = Reports.get_monthly_summary(year, month)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", f"${summary['total_income']:,.2f}")
    
    with col2:
        st.metric("Total Expenses", f"${summary['total_expenses']:,.2f}")
    
    with col3:
        st.metric("Net Balance", f"${summary['net_balance']:,.2f}",
                 delta=f"{summary['net_balance']:,.2f}")
    
    with col4:
        st.metric("Transactions", summary['transaction_count'])
    
    st.markdown("---")
    
    # Category Overview - Income and Expenses
    st.subheader("📈 Category Overview - Income & Expenses")
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Get income and expense summaries by category
    income_by_category = Transaction.get_summary_by_category(start_date, end_date, 'income')
    expense_by_category = Transaction.get_summary_by_category(start_date, end_date, 'expense')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Income by Category")
        if income_by_category:
            income_df = pd.DataFrame(income_by_category)
            income_df = income_df[['category_name', 'total_amount', 'transaction_count']]
            income_df.columns = ['Category', 'Amount', 'Count']
            income_df['Amount'] = income_df['Amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(income_df, use_container_width=True, hide_index=True)
            
            # Income pie chart
            fig_income = Reports.get_category_spending_chart(start_date, end_date, 'income')
            st.plotly_chart(fig_income, use_container_width=True)
        else:
            st.info("No income transactions this month")
    
    with col2:
        st.markdown("### 💸 Expenses by Category")
        if expense_by_category:
            expense_df = pd.DataFrame(expense_by_category)
            expense_df = expense_df[['category_name', 'total_amount', 'transaction_count']]
            expense_df.columns = ['Category', 'Amount', 'Count']
            expense_df['Amount'] = expense_df['Amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(expense_df, use_container_width=True, hide_index=True)
            
            # Expense pie chart
            fig_expense = Reports.get_category_spending_chart(start_date, end_date, 'expense')
            st.plotly_chart(fig_expense, use_container_width=True)
        else:
            st.info("No expense transactions this month")
    
    st.markdown("---")
    
    # Budget vs Actual
    st.subheader("Budget vs Actual Spending")
    budget_data = Budget.get_budget_vs_actual(year, month)
    
    if budget_data:
        budget_df = pd.DataFrame(budget_data)
        
        # Display budget status
        col1, col2 = st.columns(2)
        
        with col1:
            fig_budget = Reports.get_budget_vs_actual_chart(year, month)
            st.plotly_chart(fig_budget, use_container_width=True)
        
        with col2:
            # Budget status table
            budget_df['status'] = budget_df.apply(
                lambda row: '✅ Under Budget' if row['difference'] >= 0 else '⚠️ Over Budget',
                axis=1
            )
            display_df = budget_df[['category_name', 'budgeted_amount', 
                                   'actual_amount', 'difference', 'status']]
            display_df.columns = ['Category', 'Budgeted', 'Actual', 'Difference', 'Status']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No budget set for this month. Go to Budget Planning to set budgets.")
    
    st.markdown("---")
    
    # Spending by category comparison
    st.subheader("Spending Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = Reports.get_category_spending_chart(start_date, end_date, 'expense')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = Reports.get_category_comparison_chart(start_date, end_date)
        st.plotly_chart(fig_bar, use_container_width=True)


def show_transactions():
    """Display and manage transactions"""
    st.header("💳 Transactions")
    
    # Quick Add Transaction - More prominent
    st.markdown("### ➕ Quick Add Transaction")
    st.info("💾 All transactions are automatically saved to the database")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            trans_date = st.date_input("Date *", value=date.today(), key="quick_date")
            description = st.text_input("Description *", key="quick_desc", placeholder="e.g., Grocery shopping")
            amount = st.number_input("Amount *", min_value=0.0, step=0.01, format="%.2f", key="quick_amount")
            transaction_type = st.radio("Type *", ["expense", "income"], horizontal=True, key="quick_type")
        
        with col2:
            categories = Category.get_all()
            category_dict = {cat['name']: cat['id'] for cat in categories}
            
            # Filter categories based on transaction type
            if transaction_type == 'income':
                income_cats = [cat for cat in categories if 'income' in cat['name'].lower() or cat['name'].lower() == 'income']
                if not income_cats:
                    income_cats = categories
                category_options = ["None"] + [cat['name'] for cat in income_cats]
            else:
                expense_cats = [cat for cat in categories if 'income' not in cat['name'].lower() or cat['name'].lower() == 'income']
                category_options = ["None"] + [cat['name'] for cat in categories]
            
            selected_category = st.selectbox(
                "Category",
                category_options,
                key="quick_category"
            )
            category_id = category_dict.get(selected_category) if selected_category != "None" else None
            account_name = st.text_input("Account Name (optional)", key="quick_account", placeholder="e.g., Checking Account")
            notes = st.text_area("Notes (optional)", key="quick_notes", placeholder="Additional details...")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("➕ Add Transaction", type="primary", use_container_width=True):
                if description and amount > 0:
                    try:
                        Transaction.create(
                            date=trans_date,
                            description=description,
                            amount=amount,
                            category_id=category_id,
                            transaction_type=transaction_type,
                            account_name=account_name,
                            notes=notes
                        )
                        st.success("✅ Transaction saved automatically!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving transaction: {str(e)}")
                else:
                    st.error("⚠️ Please fill in all required fields (marked with *)")
        
        with col2:
            if st.button("🔄 Clear Form", use_container_width=True):
                st.rerun()
    
    st.markdown("---")
    
    # Filter transactions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_start = st.date_input("Start Date", value=date(st.session_state.current_year, 
                                                              st.session_state.current_month, 1))
    
    with col2:
        if st.session_state.current_month == 12:
            filter_end = st.date_input("End Date", value=date(st.session_state.current_year + 1, 1, 1))
        else:
            filter_end = st.date_input("End Date", value=date(st.session_state.current_year, 
                                                              st.session_state.current_month + 1, 1))
    
    with col3:
        categories = Category.get_all()
        category_options = ["All"] + [cat['name'] for cat in categories]
        selected_category_filter = st.selectbox("Category Filter", category_options)
    
    # Get transactions
    category_id_filter = None
    if selected_category_filter != "All":
        category_id_filter = next(
            (cat['id'] for cat in categories if cat['name'] == selected_category_filter),
            None
        )
    
    transactions = Transaction.get_all(
        start_date=filter_start,
        end_date=filter_end,
        category_id=category_id_filter
    )
    
    if transactions:
        # Display transactions
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df[['date', 'description', 'amount', 'category_name', 
                'transaction_type', 'account_name', 'notes']]
        df.columns = ['Date', 'Description', 'Amount', 'Category', 
                     'Type', 'Account', 'Notes']
        
        # Format amount
        df['Amount'] = df.apply(
            lambda row: f"${row['Amount']:,.2f}" if row['Type'] == 'expense' 
            else f"+${row['Amount']:,.2f}",
            axis=1
        )
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Summary
        total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
        total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
        with col2:
            st.metric("Total Income", f"${total_income:,.2f}")
    else:
        st.info("No transactions found for the selected period.")


def show_budget_planning():
    """Display budget planning interface"""
    st.header("📅 Budget Planning")
    
    year = st.session_state.current_year
    month = st.session_state.current_month
    
    st.subheader(f"Budget for {datetime(year, month, 1).strftime('%B %Y')}")
    
    # Get existing budgets
    existing_budgets = Budget.get_by_month(year, month)
    budget_dict = {b['category_id']: b['amount'] for b in existing_budgets}
    
    # Budget input form
    categories = Category.get_all()
    
    st.markdown("### Set Monthly Budgets")
    
    # Create form for budget entry
    with st.form("budget_form"):
        budget_data = {}
        
        # Display categories in columns
        cols = st.columns(3)
        for idx, category in enumerate(categories):
            col = cols[idx % 3]
            current_budget = budget_dict.get(category['id'], 0.0)
            budget_amount = col.number_input(
                f"{category['name']}",
                min_value=0.0,
                value=float(current_budget),
                step=10.0,
                format="%.2f",
                key=f"budget_{category['id']}"
            )
            budget_data[category['id']] = budget_amount
        
        submitted = st.form_submit_button("Save Budgets")
        
        if submitted:
            for cat_id, amount in budget_data.items():
                if amount > 0:
                    Budget.create(cat_id, year, month, amount)
            st.success("✅ Budgets saved automatically!")
            st.rerun()
    
    st.markdown("---")
    
    # Budget vs Actual
    st.subheader("Budget vs Actual")
    budget_vs_actual = Budget.get_budget_vs_actual(year, month)
    
    if budget_vs_actual:
        budget_df = pd.DataFrame(budget_vs_actual)
        budget_df['percentage_used'] = budget_df['percentage_used'].round(2)
        budget_df['status'] = budget_df.apply(
            lambda row: '✅' if row['percentage_used'] <= 100 else '⚠️',
            axis=1
        )
        
        display_df = budget_df[['category_name', 'budgeted_amount', 
                               'actual_amount', 'difference', 'percentage_used', 'status']]
        display_df.columns = ['Category', 'Budgeted', 'Actual', 'Difference', 
                            '% Used', 'Status']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Visual chart
        fig = Reports.get_budget_vs_actual_chart(year, month)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Set budgets above to see budget vs actual comparison.")


def show_reports():
    """Display reports and analytics"""
    st.header("📈 Reports & Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        report_start = st.date_input("Start Date", value=date(st.session_state.current_year, 1, 1))
    
    with col2:
        report_end = st.date_input("End Date", value=date(st.session_state.current_year, 12, 31))
    
    st.markdown("---")
    
    # Spending trends
    st.subheader("Spending Trends")
    fig_trend = Reports.get_spending_trend_chart(report_start, report_end)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # Category breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending by Category")
        fig_pie = Reports.get_category_spending_chart(report_start, report_end)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Category Comparison")
        fig_bar = Reports.get_category_comparison_chart(report_start, report_end)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Monthly comparison
    st.subheader("Monthly Comparison")
    num_months = st.slider("Number of months to compare", 3, 12, 6)
    fig_monthly = Reports.get_monthly_comparison(
        st.session_state.current_year,
        st.session_state.current_month,
        num_months
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    st.markdown("---")
    
    # Export option
    st.subheader("Export Data")
    if st.button("Export Transactions to CSV"):
        output_path = Reports.export_to_csv(report_start, report_end)
        with open(output_path, 'rb') as f:
            st.download_button(
                label="Download CSV",
                data=f.read(),
                file_name=output_path,
                mime="text/csv"
            )


def show_categories():
    """Manage categories"""
    st.header("📁 Categories")
    
    # Add new category
    with st.expander("➕ Add New Category", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            new_category_name = st.text_input("Category Name")
        
        with col2:
            new_category_desc = st.text_input("Description (optional)")
        
        if st.button("Add Category"):
            if new_category_name:
                try:
                    Category.create(new_category_name, new_category_desc)
                    st.success("✅ Category saved automatically!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Please enter a category name.")
    
    st.markdown("---")
    
    # Display categories
    categories = Category.get_all()
    
    if categories:
        df = pd.DataFrame(categories)
        df = df[['name', 'description']]
        df.columns = ['Category Name', 'Description']
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No categories found.")


def show_goals():
    """Manage financial goals"""
    st.header("🎯 Financial Goals")
    
    # Add new goal
    with st.expander("➕ Add New Goal", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input("Goal Name")
            target_amount = st.number_input("Target Amount", min_value=0.0, step=100.0, format="%.2f")
        
        with col2:
            target_date = st.date_input("Target Date (optional)", value=None)
            goal_description = st.text_area("Description (optional)")
        
        if st.button("Add Goal"):
            if goal_name and target_amount > 0:
                Goal.create(goal_name, target_amount, target_date, goal_description)
                st.success("✅ Goal saved automatically!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("---")
    
    # Display goals
    goals = Goal.get_all()
    
    if goals:
        for goal in goals:
            with st.container():
                progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(goal['name'])
                    if goal['description']:
                        st.caption(goal['description'])
                    
                    st.progress(min(progress / 100, 1.0))
                    st.caption(f"${goal['current_amount']:,.2f} / ${goal['target_amount']:,.2f} ({progress:.1f}%)")
                    
                    if goal['target_date']:
                        st.caption(f"Target Date: {goal['target_date']}")
                
                with col2:
                    new_amount = st.number_input(
                        "Update Progress",
                        min_value=0.0,
                        value=float(goal['current_amount']),
                        step=100.0,
                        format="%.2f",
                        key=f"goal_{goal['id']}"
                    )
                    if st.button("Update", key=f"update_{goal['id']}"):
                        Goal.update_progress(goal['id'], new_amount)
                        st.success("✅ Progress saved automatically!")
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_{goal['id']}"):
                        Goal.delete(goal['id'])
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No goals set. Create a goal to start tracking your progress!")


def show_import_data():
    """Import transactions from CSV or PDF"""
    st.header("📥 Import Data")
    
    st.markdown("### Import from CSV or PDF")
    st.info("""
    **CSV Format:** Your CSV should have columns: date, description, amount
    Optional columns: category, type, account, notes
    
    **PDF:** Upload bank statement PDFs. The system will attempt to extract transactions.
    """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'pdf'],
        help="Upload CSV or PDF file"
    )
    
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        file_type = uploaded_file.type
        
        # Preview option
        preview = st.checkbox("Preview before importing", value=True)
        
        if file_type == 'text/csv' or uploaded_file.name.endswith('.csv'):
            # CSV import
            importer = CSVImporter()
            
            if preview:
                result = importer.import_transactions(file_content, preview=True)
                
                if result['success']:
                    st.success(f"Found {result['count']} transactions")
                    
                    if result['preview']:
                        preview_df = pd.DataFrame(result['preview'])
                        preview_df['date'] = pd.to_datetime(preview_df['date']).dt.date
                        st.dataframe(preview_df, use_container_width=True)
                        
                        if st.button("Import All Transactions"):
                            import_result = importer.import_transactions(file_content, preview=False)
                            if import_result['success']:
                                st.success(f"✅ Successfully imported {import_result['imported']} transactions - All data saved automatically!")
                                if import_result['skipped'] > 0:
                                    st.warning(f"Skipped {import_result['skipped']} transactions")
                                if import_result['errors']:
                                    st.error("Some errors occurred:")
                                    for error in import_result['errors'][:5]:
                                        st.text(error)
                                st.balloons()
                                st.rerun()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            else:
                result = importer.import_transactions(file_content, preview=False)
                if result['success']:
                    st.success(f"✅ Successfully imported {result['imported']} transactions - All data saved automatically!")
                    if result['skipped'] > 0:
                        st.warning(f"Skipped {result['skipped']} transactions")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
        
        elif file_type == 'application/pdf' or uploaded_file.name.endswith('.pdf'):
            # PDF import
            importer = PDFImporter()
            
            if preview:
                result = importer.import_transactions(file_content, preview=True)
                
                if result['success']:
                    st.success(f"Found {result['count']} transactions")
                    
                    if result['preview']:
                        preview_df = pd.DataFrame(result['preview'])
                        preview_df['date'] = pd.to_datetime(preview_df['date']).dt.date
                        st.dataframe(preview_df, use_container_width=True)
                        
                        if st.button("Import All Transactions"):
                            import_result = importer.import_transactions(file_content, preview=False)
                            if import_result['success']:
                                st.success(f"✅ Successfully imported {import_result['imported']} transactions - All data saved automatically!")
                                if import_result['skipped'] > 0:
                                    st.warning(f"Skipped {import_result['skipped']} transactions")
                                st.balloons()
                                st.rerun()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            else:
                result = importer.import_transactions(file_content, preview=False)
                if result['success']:
                    st.success(f"✅ Successfully imported {result['imported']} transactions - All data saved automatically!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()

