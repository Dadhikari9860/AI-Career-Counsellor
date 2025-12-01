# ⚡ Quick Start Guide

Get your Career Guidance System running in 5 minutes!

---

## 🚀 Fast Setup (3 Steps)

### Step 1: Start Backend (Terminal 1)

```bash
cd /home/dinesh/FinalYearProject/backend
source venv/bin/activate
python run.py
```

✅ Wait for: `Running on http://127.0.0.1:5000`

### Step 2: Start Frontend (Terminal 2 - New Window)

```bash
cd /home/dinesh/FinalYearProject/frontend
npm run dev
```

✅ Wait for: `Local: http://localhost:3001/`

### Step 3: Open Browser

```
http://localhost:3001
```

---

## 🎯 That's It!

1. **Register** a new account
2. **Set your target role** in Profile
3. **Explore** the dashboard!

---

## ❓ Common Issues

### Backend won't start?

```bash
cd backend
source venv/bin/activate
pip install -r requirements-minimal.txt
python run.py
```

### Frontend won't start?

```bash
cd frontend
npm install
npm run dev
```

### Need to train models?

```bash
cd backend
source venv/bin/activate
python scripts/create_and_train_datasets.py
```

---

## 📚 More Details

See `HOW_TO_RUN.md` for complete setup instructions.
