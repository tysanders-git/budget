# Quick Deploy to Phone - 5 Minutes!

## Easiest Way: Streamlit Cloud

### Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `family-budget-tracker`
3. Make it **Public** (required for free Streamlit Cloud)
4. Click "Create repository"

### Step 2: Upload Your Code (2 minutes)

**Using GitHub Desktop (Easiest):**
1. Download: https://desktop.github.com
2. Install and sign in
3. File → Add Local Repository
4. Select: `C:\Users\Tyler\family_budget_tracker`
5. Click "Publish repository"
6. Make sure it's **Public**
7. Click "Publish repository"

**OR Using Command Line:**
```bash
cd C:\Users\Tyler\family_budget_tracker
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/family-budget-tracker.git
git push -u origin main
```
(Replace YOUR_USERNAME with your GitHub username)

### Step 3: Deploy to Streamlit Cloud (1 minute)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `family-budget-tracker`
5. Main file path: `app.py`
6. Click "Deploy"
7. Wait 2-3 minutes

### Step 4: Access on Your Phone!

- You'll get a URL like: `https://family-budget-tracker.streamlit.app`
- Open it on your phone's browser
- **Bookmark it!**
- Works on any device, anywhere!

---

## Alternative: ngrok (For Quick Testing)

If you just want to test on your phone right now:

1. **Download ngrok**: https://ngrok.com/download
2. **Sign up** for free account (get auth token)
3. **Start your app**:
   ```bash
   cd C:\Users\Tyler\family_budget_tracker
   streamlit run app.py
   ```
4. **In a new terminal**, run:
   ```bash
   ngrok http 8501
   ```
5. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
6. **Open on your phone**!

**Note:** This only works while your computer is running. For permanent access, use Streamlit Cloud above.

---

## That's It!

Your budget tracker will be accessible on your phone! 📱💰

