@echo off
echo ========================================
echo Family Budget Tracker - Deployment Setup
echo ========================================
echo.
echo This script will help you prepare your app for deployment.
echo.
echo Step 1: Make sure you have GitHub Desktop installed
echo        Download from: https://desktop.github.com
echo.
echo Step 2: Create a GitHub repository at: https://github.com/new
echo        Name: family-budget-tracker
echo        Make it PUBLIC (required for free Streamlit Cloud)
echo.
echo Step 3: Use GitHub Desktop to publish this folder
echo        File -^> Add Local Repository
echo        Select: %CD%
echo        Click "Publish repository"
echo.
echo Step 4: Deploy to Streamlit Cloud
echo        Go to: https://share.streamlit.io
echo        Sign in with GitHub
echo        Click "New app"
echo        Select your repository
echo        Main file: app.py
echo        Click "Deploy"
echo.
echo ========================================
echo.
echo Your files are ready for deployment!
echo.
echo See SETUP_FOR_DEPLOYMENT.md for detailed instructions.
echo.
pause

