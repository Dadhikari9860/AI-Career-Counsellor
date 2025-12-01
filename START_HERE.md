# 🎯 START HERE - How to Run Your Project

## ⚡ Super Quick Start (2 Minutes)

### Step 1: Open Terminal 1

```bash
cd /home/dinesh/FinalYearProject
./start_backend.sh
```

**Wait for:** `Running on http://127.0.0.1:5000`

### Step 2: Open Terminal 2 (New Window)

```bash
cd /home/dinesh/FinalYearProject
./start_frontend.sh
```

**Wait for:** `Local: http://localhost:3001/`

### Step 3: Open Browser

Go to: **http://localhost:3001**

**Done!** 🎉

---

## 📝 Detailed Step-by-Step

### 🔧 Backend Setup (First Time Only)

If you haven't set up before:

```bash
# 1. Go to backend directory
cd /home/dinesh/FinalYearProject/backend

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies (if not installed)
pip install -r requirements-minimal.txt

# 4. Train ML models (first time only - takes 5-10 minutes)
python scripts/create_and_train_datasets.py
```

### 🎨 Frontend Setup (First Time Only)

If you haven't set up before:

```bash
# 1. Go to frontend directory
cd /home/dinesh/FinalYearProject/frontend

# 2. Install dependencies (if not installed)
npm install
```

---

## 🚀 Running the Project (Every Time)

### Method 1: Using Scripts (Recommended)

**Terminal 1:**

```bash
cd /home/dinesh/FinalYearProject
./start_backend.sh
```

**Terminal 2 (New Window):**

```bash
cd /home/dinesh/FinalYearProject
./start_frontend.sh
```

### Method 2: Manual Commands

**Terminal 1 - Backend:**

```bash
cd /home/dinesh/FinalYearProject/backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**

```bash
cd /home/dinesh/FinalYearProject/frontend
npm run dev
```

---

## ✅ What You Should See

### Backend Terminal:

```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### Frontend Terminal:

```
  VITE v5.4.21  ready in XXX ms
  ➜  Local:   http://localhost:3001/
```

### Browser:

- Login/Register page with modern design
- Google Sign-In button (if configured)

---

## 🎯 First Steps After Opening

1. **Register** a new account
2. **Login** with your credentials
3. **Go to Profile** → Set your target role (e.g., "Full Stack Developer")
4. **Upload Resume** (optional) → Profile → Resume Upload
5. **Explore Dashboard** → See recommendations!

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"

```bash
cd backend
source venv/bin/activate
pip install -r requirements-minimal.txt
```

### "Port already in use"

- Backend: Kill process on port 5000 or use different port
- Frontend: Vite will automatically use port 3001 if 3000 is busy

### "Models not found"

```bash
cd backend
source venv/bin/activate
python scripts/create_and_train_datasets.py
```

### "Cannot connect to backend"

- Make sure backend is running on port 5000
- Check browser console (F12) for errors
- Verify both servers are running

---

## 📚 More Help

- **Complete Guide:** See `HOW_TO_RUN.md`
- **Quick Reference:** See `QUICK_START.md`
- **Google OAuth Setup:** See `GOOGLE_OAUTH_SETUP.md`

---

## 🎉 You're Ready!

Just run the two startup scripts and open your browser. That's it!
