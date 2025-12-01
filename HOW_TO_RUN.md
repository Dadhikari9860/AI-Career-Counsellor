# 🚀 How to Run the Career Guidance System

Complete guide to set up and run the project from scratch.

---

## 📋 Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed
- **Node.js 16+** and **npm** installed
- **Git** installed (optional)
- **Virtual environment** (recommended)

---

## 🔧 Step 1: Backend Setup

### 1.1 Navigate to Backend Directory

```bash
cd /home/dinesh/FinalYearProject/backend
```

### 1.2 Create and Activate Virtual Environment

```bash
# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install Python Dependencies

```bash
# Install minimal requirements first
pip install -r requirements-minimal.txt

# If you have space, install optional packages
# pip install -r requirements-optional.txt
```

**Note:** If you get disk space errors, just install the minimal requirements.

### 1.4 Set Up Environment Variables (Optional)

Create a `.env` file in the `backend` directory:

```bash
cd /home/dinesh/FinalYearProject/backend
nano .env
```

Add these lines (optional - defaults will be used if not set):

```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///career_guidance.db
GOOGLE_CLIENT_ID=your-google-client-id-here  # Optional for Google login
```

Save and exit (Ctrl+X, then Y, then Enter).

### 1.5 Train ML Models (First Time Only)

```bash
# Make sure you're in the backend directory with venv activated
cd /home/dinesh/FinalYearProject/backend
source venv/bin/activate

# Run the training script
python scripts/create_and_train_datasets.py
```

This will:

- Create synthetic datasets
- Train all ML models
- Save models to `ml/models/` directory

**Time:** This may take 5-10 minutes depending on your system.

### 1.6 Start Backend Server

```bash
# Make sure venv is activated
source venv/bin/activate

# Start the server
python run.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

**Keep this terminal open!** The backend server must be running.

---

## 🎨 Step 2: Frontend Setup

### 2.1 Open a New Terminal Window

Keep the backend terminal running, open a **new terminal window**.

### 2.2 Navigate to Frontend Directory

```bash
cd /home/dinesh/FinalYearProject/frontend
```

### 2.3 Install Node Dependencies

```bash
npm install
```

This may take a few minutes the first time.

### 2.4 Start Frontend Development Server

```bash
npm run dev
```

You should see:

```
  VITE v5.4.21  ready in XXX ms
  ➜  Local:   http://localhost:3001/
```

**Note:** If port 3000 is busy, Vite will use 3001 automatically.

---

## 🌐 Step 3: Access the Application

1. **Open your web browser**
2. **Go to:** `http://localhost:3001` (or `http://localhost:3000`)
3. **You should see the login page**

---

## 👤 Step 4: Create Your First Account

### Option A: Register New Account

1. Click **"Register Now"** link on login page
2. Fill in:
   - Full Name
   - Location (e.g., "Kathmandu, Bagmati")
   - Username
   - Email
   - Password
3. Click **"Create Account"**
4. You'll be automatically logged in and redirected to dashboard

### Option B: Use Google Login (Optional)

1. Set up Google OAuth (see `GOOGLE_OAUTH_SETUP.md`)
2. Set `GOOGLE_CLIENT_ID` environment variable
3. Restart backend server
4. Google Sign-In button will appear on login page

---

## ✅ Step 5: Verify Everything Works

After logging in, you should see:

- ✅ **Dashboard** with welcome message
- ✅ **Recommended Roles** section
- ✅ **Recommended Jobs** section (with LinkedIn links)
- ✅ **Learning Resources** section (with YouTube links)
- ✅ **Skill Gap Analysis** (if target role is set)

---

## 🔄 Quick Start Commands (Summary)

### Terminal 1 - Backend:

```bash
cd /home/dinesh/FinalYearProject/backend
source venv/bin/activate
python run.py
```

### Terminal 2 - Frontend:

```bash
cd /home/dinesh/FinalYearProject/frontend
npm run dev
```

### Then open browser:

```
http://localhost:3001
```

---

## 🐛 Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'flask'"

```bash
cd backend
source venv/bin/activate
pip install -r requirements-minimal.txt
```

#### "ModuleNotFoundError: No module named 'google.oauth2'"

This is **OK** - Google OAuth is optional. The server will still run without it.
To enable Google login:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

#### "Port 5000 already in use"

```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Or use a different port
export FLASK_RUN_PORT=5001
python run.py
```

#### "Database errors"

```bash
cd backend
source venv/bin/activate
python
>>> from app import create_app, db
>>> from config import Config
>>> app = create_app(Config)
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Frontend Issues

#### "Port 3000 is in use"

Vite will automatically use port 3001. Just use that URL instead.

#### "npm install fails"

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### "Cannot connect to backend"

- Check backend is running on port 5000
- Check `vite.config.ts` has correct proxy settings
- Check browser console for CORS errors

### ML Model Issues

#### "Models not found"

```bash
cd backend
source venv/bin/activate
python scripts/create_and_train_datasets.py
```

#### "Low accuracy"

The models are pre-trained. If you want to retrain:

```bash
cd backend
source venv/bin/activate
python scripts/create_and_train_datasets.py
```

---

## 📁 Project Structure

```
FinalYearProject/
├── backend/
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models.py      # Database models
│   │   └── __init__.py    # Flask app factory
│   ├── ml/
│   │   ├── models/        # Trained ML models
│   │   └── training/      # Training scripts
│   ├── data/              # Datasets
│   ├── requirements-minimal.txt
│   └── run.py            # Server entry point
├── frontend/
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   └── services/      # API services
│   └── package.json
└── README.md
```

---

## 🔐 Default Configuration

- **Backend URL:** `http://localhost:5000`
- **Frontend URL:** `http://localhost:3001` (or 3000)
- **Database:** SQLite (`career_guidance.db` in backend directory)
- **JWT Expiry:** 24 hours

---

## 🎯 Next Steps After Running

1. **Set Target Role:** Go to Profile → Set your target career role
2. **Upload Resume:** Profile → Resume Upload → Upload your resume
3. **Explore Dashboard:** See personalized recommendations
4. **Use Chatbot:** Ask questions about careers, skills, jobs
5. **Check Skill Gaps:** See what skills you need to learn
6. **View Learning Resources:** Get YouTube links for missing skills

---

## 📞 Need Help?

- Check terminal logs for errors
- Check browser console (F12) for frontend errors
- Verify both servers are running
- Make sure ports 5000 and 3001 are not blocked

---

## 🚀 Production Deployment

For production:

1. Set `FLASK_ENV=production`
2. Use PostgreSQL instead of SQLite
3. Set proper `SECRET_KEY` and `JWT_SECRET_KEY`
4. Update CORS origins in `config.py`
5. Use a production WSGI server (gunicorn)
6. Build frontend: `npm run build`
7. Serve frontend with nginx or similar

---

**Happy coding! 🎉**
