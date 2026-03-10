# 🚀 Deployment Guide for Streamlit Community Cloud

Follow these steps to deploy your Medical Insurance Premium Predictor and get a **shareable public URL**.

## Prerequisites
- ✅ GitHub account
- ✅ Streamlit Community Cloud account (free at https://streamlit.io/cloud)

---

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `medical-insurance-predictor` (or any name you prefer)
   - **Visibility**: Public ✅
   - **Don't** initialize with README (we already have one)
3. Click "Create repository"

---

## Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd C:\Users\Ayush.Diyundi\DHBW_Python\MedicalPremiumproject
git remote add origin https://github.com/YOUR_USERNAME/medical-insurance-predictor.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 3: Deploy to Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Fill in the details:
   - **Repository**: Select `YOUR_USERNAME/medical-insurance-predictor`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click "Deploy!"

⏳ Wait 2-3 minutes for deployment...

---

## Step 4: Get Your Shareable URL

Once deployed, you'll receive a public URL like:

```
https://YOUR_USERNAME-medical-insurance-predictor-app-XXXXXX.streamlit.app
```

✅ **THIS URL IS SHAREABLE WITH ANYONE IN THE WORLD!**

---

## Files Included in This Repository

✅ `app.py` - Main application
✅ `requirements.txt` - Python dependencies
✅ `medical_premium_model.pkl` - Trained model
✅ `model_columns.pkl` - Feature names
✅ `Medicalpremium.csv` - Dataset
✅ `README.md` - Documentation
✅ `.gitignore` - Git ignore rules

---

## Troubleshooting

### If deployment fails:

1. **Check requirements.txt** - Make sure all versions are compatible
2. **Check file paths** - Ensure all files are in the same directory
3. **Check model files** - Ensure .pkl files are committed to GitHub
4. **View logs** - Click "Manage app" → "Logs" in Streamlit Cloud

### Common Issues:

- **"Module not found"** → Add the missing package to `requirements.txt`
- **"File not found"** → Make sure all files are pushed to GitHub
- **"Memory error"** → Your model might be too large (unlikely for this project)

---

## Alternative: Quick Test Locally

Before deploying, test locally:

```bash
cd C:\Users\Ayush.Diyundi\DHBW_Python\MedicalPremiumproject
C:\Users\Ayush.Diyundi\AppData\Local\Python\pythoncore-3.14-64\Scripts\streamlit.exe run app.py
```

The **Network URL** shown can be shared with people on your WiFi.

---

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- GitHub Docs: https://docs.github.com/en/get-started

---

**Happy Deploying! 🎉**

