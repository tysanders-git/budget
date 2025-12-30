# Mobile Access Deployment Guide

## Option 1: Streamlit Cloud (Recommended - Free & Permanent)

Streamlit Cloud is the easiest way to make your app accessible on your phone and any device.

### Steps:

1. **Create a GitHub Account** (if you don't have one)
   - Go to https://github.com
   - Sign up for a free account

2. **Create a GitHub Repository**
   - Click "New repository"
   - Name it: `family-budget-tracker`
   - Make it Public (required for free Streamlit Cloud)
   - Don't initialize with README
   - Click "Create repository"

3. **Upload Your Code to GitHub**
   
   **Option A: Using GitHub Desktop (Easiest)**
   - Download GitHub Desktop: https://desktop.github.com
   - Install and sign in
   - Click "File" > "Add Local Repository"
   - Select your `family_budget_tracker` folder
   - Click "Publish repository"
   - Make it public
   - Click "Publish repository"

   **Option B: Using Git Command Line**
   ```bash
   cd C:\Users\Tyler\family_budget_tracker
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/family-budget-tracker.git
   git push -u origin main
   ```

4. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `family-budget-tracker`
   - Main file path: `app.py`
   - Click "Deploy"
   - Wait 2-3 minutes for deployment

5. **Access on Your Phone**
   - Streamlit Cloud will give you a URL like: `https://your-app-name.streamlit.app`
   - Open this URL on your phone's browser
   - Bookmark it for easy access!

### Benefits:
- ✅ Free forever
- ✅ Accessible from anywhere
- ✅ Auto-updates when you push to GitHub
- ✅ Works on any device (phone, tablet, computer)
- ✅ Secure and reliable

---

## Option 2: ngrok (Quick Local Access - Temporary)

This makes your local app accessible on your phone while your computer is running.

### Steps:

1. **Install ngrok**
   - Go to https://ngrok.com
   - Sign up for free account
   - Download ngrok for Windows
   - Extract to a folder (e.g., `C:\ngrok`)

2. **Start Your Streamlit App**
   ```bash
   cd C:\Users\Tyler\family_budget_tracker
   streamlit run app.py
   ```
   Note the port (usually 8501)

3. **Create ngrok Tunnel**
   - Open a new terminal
   - Run: `ngrok http 8501`
   - Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

4. **Access on Phone**
   - Open the ngrok URL on your phone
   - Note: URL changes each time you restart ngrok (unless you have a paid plan)

### Limitations:
- ⚠️ Only works when your computer is on
- ⚠️ URL changes each restart (free plan)
- ⚠️ Temporary solution

---

## Option 3: Deploy to Heroku (More Complex)

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   port = $PORT\n\
   enableCORS = false\n\
   headless = true\n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku (requires Heroku account)

---

## Option 4: Convert to Mobile App (Advanced)

You could convert this to a native mobile app using:
- **Streamlit Mobile** (experimental)
- **Python-to-Android** tools (Kivy, BeeWare)
- **Web-to-App** wrappers (PWA, Capacitor)

This is more complex and may require significant code changes.

---

## Recommended: Streamlit Cloud

**For the easiest, permanent solution, use Streamlit Cloud (Option 1).**

Your app will be accessible at a URL like:
`https://family-budget-tracker.streamlit.app`

You can:
- Access it from any device
- Share it with family members
- Use it anywhere with internet
- It's free and reliable

---

## Quick Start Commands

If you want to use GitHub:

```bash
# Navigate to your project
cd C:\Users\Tyler\family_budget_tracker

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Family Budget Tracker App"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/family-budget-tracker.git

# Push to GitHub
git push -u origin main
```

Then deploy on Streamlit Cloud!

