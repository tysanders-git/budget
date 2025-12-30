# Family Budget Tracker 2026

A comprehensive family household spending tracker and budget planning tool built with Python, Streamlit, and SQLite.

## Features

### Core Functionality
- **Transaction Management**: Add, view, edit, and delete income and expense transactions
- **Budget Planning**: Set monthly budgets by category and track budget vs actual spending
- **Category Management**: Organize transactions with customizable categories
- **Reports & Analytics**: Visual charts and reports for spending analysis
- **Financial Goals**: Set and track progress toward financial goals
- **Data Import**: Import transactions from CSV files or PDF bank statements
- **Auto-Save**: All data is automatically saved to SQLite database

### Key Features
- 📊 **Dashboard**: Overview of income, expenses, and budget status with category breakdowns
- 💳 **Transaction Tracker**: Comprehensive transaction management with filtering
- 📅 **Budget Planning**: Set and monitor monthly budgets by category
- 📈 **Reports**: Multiple visualization types (pie charts, bar charts, trend lines)
- 🎯 **Goals**: Track progress toward financial goals
- 📥 **Import**: Support for CSV and PDF file imports
- 📁 **Categories**: Customizable spending categories
- 💾 **Auto-Save**: All data automatically saved - persists through refreshes

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Start using the application**:
   - Navigate through different pages using the sidebar
   - Add transactions manually or import from CSV/PDF
   - Set budgets for each category
   - View reports and analytics

## 📱 Access on Your Phone

**Want to use this app on your phone?** 

### Quick Setup (5 minutes):
1. Install GitHub Desktop: https://desktop.github.com
2. Create a GitHub repository (make it public)
3. Upload your code using GitHub Desktop
4. Deploy to Streamlit Cloud: https://share.streamlit.io
5. Access from any device!

**See `SETUP_FOR_DEPLOYMENT.md` for detailed step-by-step instructions!**

## Project Structure

```
family_budget_tracker/
├── app.py              # Main Streamlit application
├── db.py               # Database initialization and connection
├── models.py           # Data models and database operations
├── csv_importer.py     # CSV file import functionality
├── pdf_importer.py     # PDF statement import functionality
├── reports.py          # Reports and visualization generation
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── budget_tracker.db  # SQLite database (created automatically)
```

## Database Schema

The application uses SQLite with the following tables:
- **categories**: Spending categories
- **transactions**: Income and expense transactions
- **budgets**: Monthly budget allocations by category
- **goals**: Financial goals and progress tracking
- **recurring_transactions**: Recurring transaction templates (for future use)

## CSV Import Format

Your CSV file should have the following columns:
- **Required**: `date`, `description`, `amount`
- **Optional**: `category`, `type` (income/expense), `account`, `notes`

Example CSV:
```csv
date,description,amount,category,type
2026-01-15,Grocery Store,125.50,Food & Groceries,expense
2026-01-16,Salary,3000.00,Income,income
```

## PDF Import

The application can extract transactions from PDF bank statements. It attempts to:
- Extract table data from structured PDFs
- Parse text-based statements
- Auto-categorize transactions based on description keywords

## Data Persistence

- ✅ All data is automatically saved to SQLite database
- ✅ Data persists through page refreshes and app restarts
- ✅ Database file: `budget_tracker.db` (in project directory)
- ✅ No manual save required - everything is auto-saved!

## License

This project is open source and available for personal use.

