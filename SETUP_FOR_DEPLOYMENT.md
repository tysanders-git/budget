# Setup for Mobile Deployment - Step by Step

## Step 1: Install GitHub Desktop (2 minutes)

1. **Download GitHub Desktop**: https://desktop.github.com
2. **Install** the application
3. **Sign in** with your GitHub account (or create one at https://github.com)

## Step 2: Create GitHub Repository (1 minute)

1. Go to https://github.com/new
2. Repository name: `family-budget-tracker`
3. Description: "Family Budget Tracker 2026 - Streamlit App"
4. Make it **PUBLIC** (required for free Streamlit Cloud)
5. **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

## Step 3: Upload Your Code with GitHub Desktop (2 minutes)

1. **Open GitHub Desktop**
2. Click **"File"** → **"Add Local Repository"**
3. Click **"Choose..."**
4. Navigate to: `C:\Users\Tyler\family_budget_tracker`
5. Click **"Add repository"**
6. You'll see all your files listed
7. At the bottom, type a commit message: "Initial commit - Family Budget Tracker"
8. Click **"Commit to main"**
9. Click **"Publish repository"** button (top right)
10. Make sure **"Keep this code private"** is **UNCHECKED** (must be public)
11. Click **"Publish repository"**

## Step 4: Deploy to Streamlit Cloud (2 minutes)

1. Go to https://share.streamlit.io
2. Click **"Sign in"** → Sign in with **GitHub**
3. Click **"New app"** button
4. Fill in:
   - **Repository**: Select `family-budget-tracker`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy"**
6. Wait 2-3 minutes for deployment

## Step 5: Access on Your Phone! 📱

1. Once deployed, you'll see a URL like: `https://family-budget-tracker.streamlit.app`
2. **Copy this URL**
3. Open it on your phone's browser
4. **Bookmark it** for easy access!

---

## Alternative: If You Prefer Command Line

If you install Git from https://git-scm.com/download/win, then run:

```bash
cd C:\Users\Tyler\family_budget_tracker
git init
git add .
git commit -m "Initial commit - Family Budget Tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/family-budget-tracker.git
git push -u origin main
```

Then follow Step 4 above.

---

## Your App Will Be Live At:

`https://YOUR-USERNAME-family-budget-tracker.streamlit.app`

Access it from:
- ✅ Your phone
- ✅ Your tablet  
- ✅ Any computer
- ✅ Anywhere with internet!

---

## Need Help?

- GitHub Desktop Guide: https://docs.github.com/en/desktop
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud

