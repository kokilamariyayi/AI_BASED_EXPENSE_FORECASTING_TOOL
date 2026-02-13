# SpendGenie Backend - Flask API
import os
import io
import uuid
import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore")

# ----------------- Configuration -----------------
# Get absolute path to the backend directory
BACKEND_DIR = Path(__file__).parent.absolute()
BASE_DIR = BACKEND_DIR / "data"
UPLOAD_ROOT = BASE_DIR / "uploads"

# Create directories with proper error handling
try:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created data directory at: {BASE_DIR}")
except Exception as e:
    print(f"ERROR creating directories: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Backend directory: {BACKEND_DIR}")
    raise

# ----------------- Flask app -----------------
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.secret_key = "spendgenie-secret-key-2025"

# Use absolute path for database
DB_PATH = BASE_DIR / "users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print(f"✓ Database will be created at: {DB_PATH}")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ----------------- Database model -----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    def check_pass(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

# Create database tables
try:
    with app.app_context():
        db.create_all()
        print(f"✓ Database initialized successfully")
        print(f"✓ Database location: {DB_PATH}")
except Exception as e:
    print(f"ERROR initializing database: {e}")
    raise

# ----------------- Utilities -----------------
def safe_session_id():
    sid = session.get("session_id")
    if not sid:
        sid = str(uuid.uuid4())
        session["session_id"] = sid
    return sid

def user_upload_dir():
    sid = safe_session_id()
    d = UPLOAD_ROOT / sid
    d.mkdir(parents=True, exist_ok=True)
    return d

def save_uploaded_csv(file_storage):
    updir = user_upload_dir()
    filename = "uploaded.csv"
    path = updir / filename
    file_storage.save(str(path))
    return str(path)

def get_user_csv_path():
    updir = user_upload_dir()
    path = updir / "uploaded.csv"
    if path.exists():
        return str(path)
    return None

def guess_col(candidates, columns):
    cols_lower = {c.lower(): c for c in columns}
    for name in candidates:
        if name.lower() in cols_lower:
            return cols_lower[name.lower()]
    for name in candidates:
        for c in columns:
            if name.lower() in c.lower():
                return c
    return None

def clean_amount_val(x):
    try:
        if pd.isna(x):
            return np.nan
        s = str(x).strip()
        if s == "":
            return np.nan
        if s.startswith("(") and s.endswith(")"):
            s = "-" + s[1:-1]
        s = s.replace(",", "")
        s2 = "".join(ch for ch in s if ch.isdigit() or ch in ".-+")
        if s2 in ("", ".", "+", "-", "+.", "-."):
            return np.nan
        return float(s2)
    except:
        return np.nan

def load_and_prepare(csv_path):
    df = pd.read_csv(csv_path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    cols = df.columns.tolist()
    date_col = guess_col(["date","transaction_date","txn_date","posted_date","timestamp"], cols)
    amt_col = guess_col(["amount","amt","value","transaction_amount","debit","credit"], cols)
    cat_col = guess_col(["category","cat","expense_category","merchant_category","type","merchant"], cols)
    desc_col = guess_col(["description","memo","narration","details"], cols)
    
    if not date_col or not amt_col:
        raise ValueError("Could not detect date and amount columns.")
    
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df["_raw_amount_"] = df[amt_col]
    df["amount_clean"] = df[amt_col].map(clean_amount_val)
    df = df.dropna(subset=["amount_clean"])
    
    if cat_col:
        df["category_clean"] = df[cat_col].fillna("Uncategorized").astype(str)
    else:
        df["category_clean"] = "Uncategorized"
    
    if desc_col:
        df["description_clean"] = df[desc_col].astype(str)
    else:
        df["description_clean"] = ""
    
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["month_year"] = df[date_col].dt.to_period("M").astype(str)
    df["day"] = df[date_col].dt.date
    
    nonzero = df[df["amount_clean"] != 0]["amount_clean"]
    neg_frac = (nonzero < 0).mean() if len(nonzero) > 0 else 0
    
    if neg_frac >= 0.5:
        df["expense"] = df["amount_clean"].apply(lambda v: -v if v < 0 else 0.0)
        df["income"] = df["amount_clean"].apply(lambda v: v if v > 0 else 0.0)
        sign_rule = "expenses_negative"
    else:
        type_col = guess_col(["type","transaction_type","kind"], cols)
        if type_col and type_col in df.columns:
            t = df[type_col].astype(str).str.lower()
            exp_mask = t.isin(["expense","debit","withdrawal","payment","spent"])
            df["expense"] = df["amount_clean"].where(exp_mask, 0).abs()
            df["income"] = df["amount_clean"].where(~exp_mask, 0).abs()
            sign_rule = "type_based"
        else:
            df["expense"] = df["amount_clean"].apply(lambda v: v if v > 0 else 0.0)
            df["income"] = df["amount_clean"].apply(lambda v: -v if v < 0 else 0.0)
            sign_rule = "positive_expense"
    
    return df, {"date_col": date_col, "amt_col": amt_col, "cat_col": cat_col, "sign_rule": sign_rule}

def aggregate_past_months(df, months_back=6):
    """Aggregate monthly expenses for prediction"""
    df = df.copy()
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum().reset_index()
    monthly['month_num'] = range(len(monthly))
    return monthly.tail(months_back)

def predict_next_total(monthly_df):
    """Predict next month's total expense using linear regression"""
    if len(monthly_df) < 2:
        return monthly_df['amount'].mean() if len(monthly_df) > 0 else 0
    
    X = monthly_df[['month_num']].values
    y = monthly_df['amount'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_month_num = monthly_df['month_num'].max() + 1
    predicted = model.predict([[next_month_num]])[0]
    
    return max(0, predicted)

# ----------------- API Routes -----------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "SpendGenie API is running"})

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    
    session["user_id"] = user.id
    session["username"] = user.username
    
    return jsonify({"message": "Registration successful", "username": user.username})

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_pass(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    session["user_id"] = user.id
    session["username"] = user.username
    
    return jsonify({"message": "Login successful", "username": user.username})

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route("/api/auth/status", methods=["GET"])
def auth_status():
    if "user_id" in session:
        return jsonify({
            "authenticated": True,
            "username": session.get("username")
        })
    return jsonify({"authenticated": False})

@app.route("/api/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files allowed"}), 400
    
    try:
        path = save_uploaded_csv(file)
        df, meta = load_and_prepare(path)
        
        return jsonify({
            "message": "File uploaded successfully",
            "rows": len(df),
            "columns": df.columns.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/analytics", methods=["GET"])
def analytics():
    path = get_user_csv_path()
    if not path:
        return jsonify({"error": "No dataset uploaded"}), 400
    
    try:
        df, meta = load_and_prepare(path)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    year = request.args.get("year")
    month = request.args.get("month")
    start = request.args.get("start")
    end = request.args.get("end")
    
    temp = df.copy()
    if year:
        try:
            temp = temp[temp["year"] == int(year)]
        except:
            pass
    if month:
        try:
            temp = temp[temp["month"] == int(month)]
        except:
            pass
    if start:
        try:
            temp = temp[temp[meta["date_col"]] >= pd.to_datetime(start)]
        except:
            pass
    if end:
        try:
            temp = temp[temp[meta["date_col"]] <= pd.to_datetime(end)]
        except:
            pass
    
    expenses = temp[temp["expense"] > 0].copy()
    
    monthly = expenses.groupby("month_year")["expense"].sum().reset_index().rename(columns={"expense":"amount"})
    category = expenses.groupby("category_clean")["expense"].sum().reset_index().rename(columns={"category_clean":"category","expense":"amount"}).sort_values("amount", ascending=False)
    peak_data = expenses.groupby("day")["expense"].sum()
    
    if len(peak_data) > 0:
        peak = peak_data.reset_index(name="amount").sort_values("amount", ascending=False).head(10)
    else:
        peak = pd.DataFrame({"day":["No Data"], "amount":[0]})
    
    yearly = expenses.groupby("year")["expense"].sum().reset_index().rename(columns={"expense":"amount"})
    
    total = float(expenses["expense"].sum()) if len(expenses) > 0 else 0.0
    top_cat = category.iloc[0]["category"] if len(category) > 0 else None
    peak_row = peak.iloc[0] if len(peak) > 0 else None
    
    summary = {
        "total": total,
        "top_cat": top_cat,
        "peak_day": str(peak_row["day"]) if peak_row is not None else None,
        "peak_amount": float(peak_row["amount"]) if peak_row is not None else 0.0
    }
    
    return jsonify({
        "monthly": monthly.to_dict(orient="records"),
        "category": category.to_dict(orient="records"),
        "peak": peak.to_dict(orient="records"),
        "yearly": yearly.to_dict(orient="records"),
        "summary": summary
    })

@app.route("/api/summary", methods=["GET"])
def summary():
    path = get_user_csv_path()
    if not path:
        return jsonify({"error": "No dataset uploaded"}), 400
    
    try:
        df, meta = load_and_prepare(path)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    year = request.args.get("year")
    month = request.args.get("month")
    start = request.args.get("start")
    end = request.args.get("end")
    
    temp = df.copy()
    if year:
        try:
            temp = temp[temp["year"] == int(year)]
        except:
            pass
    if month:
        try:
            temp = temp[temp["month"] == int(month)]
        except:
            pass
    if start:
        try:
            temp = temp[temp[meta["date_col"]] >= pd.to_datetime(start)]
        except:
            pass
    if end:
        try:
            temp = temp[temp[meta["date_col"]] <= pd.to_datetime(end)]
        except:
            pass
    
    expenses = temp[temp["expense"] > 0]
    if len(expenses) == 0:
        return jsonify({"summary": "No data available for the selected period."})
    
    total = float(expenses["expense"].sum())
    cat_sums = expenses.groupby("category_clean")["expense"].sum().sort_values(ascending=False)
    top_cat = cat_sums.index[0]
    top_amt = cat_sums.iloc[0]
    
    insight_lines = [
        f"🧠 AI Summary (filtered range)",
        f"• Total spending: ₹{total:,.2f}",
        f"• Top category: {top_cat} (₹{top_amt:,.2f})",
    ]
    
    try:
        last_month = expenses["month_year"].max()
        prev = expenses[expenses["month_year"] < last_month].groupby("month_year")["expense"].sum()
        last_val = expenses[expenses["month_year"]==last_month]["expense"].sum()
        prev_mean = prev.mean() if len(prev) > 0 else 0
        if prev_mean > 0:
            pct = (last_val - prev_mean) / prev_mean * 100
            if pct > 10:
                insight_lines.append(f"• Spending increased ~{pct:.0f}% vs previous months — review {top_cat}.")
            elif pct < -10:
                insight_lines.append("• Spending decreased compared with previous months — good job!")
    except Exception:
        pass
    
    insight_lines.append("• Suggestion: set a limit for the top category to reduce recurring spend.")
    
    return jsonify({"summary": "\n".join(insight_lines)})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    msg = (data.get("message") or "").lower().strip()
    reply = "Sorry, I couldn't understand. Try: 'top categories', 'monthly trend', 'reduce dining', or 'save more'."
    
    path = get_user_csv_path()
    df = None
    meta = None
    
    try:
        if path:
            df, meta = load_and_prepare(path)
    except Exception:
        df = None
    
    if "top category" in msg or "top categories" in msg or "top spend" in msg:
        if df is None:
            reply = "I don't see a dataset yet. Upload your CSV to get started."
        else:
            cat_sums = df.groupby("category_clean")["expense"].sum().sort_values(ascending=False)
            top = cat_sums.head(3).to_dict()
            lines = ["Top spending categories:"]
            for k, v in top.items():
                lines.append(f"• {k}: ₹{v:,.2f}")
            reply = "\n".join(lines)
    
    elif "monthly" in msg or "trend" in msg:
        if df is None:
            reply = "No data yet — upload a CSV to get monthly trends."
        else:
            monthly = df.groupby("month_year")["expense"].sum().sort_index()
            if len(monthly) == 0:
                reply = "No expense data found in the file."
            else:
                last = monthly.iloc[-1]
                mean_prev = monthly.iloc[:-1].mean() if len(monthly) > 1 else monthly.iloc[-1]
                if mean_prev > 0:
                    pct = (last - mean_prev) / mean_prev * 100
                    reply = f"Latest month total: ₹{last:,.2f}. That's {pct:+.0f}% vs average of prior months."
                else:
                    reply = f"Latest month total: ₹{last:,.2f}."
    
    elif "reduce" in msg or "save" in msg or "cut" in msg:
        tips = [
            "Track subscriptions and cancel unused ones.",
            "Set a weekly dining out limit and carry cash for it.",
            "Automate a small transfer to savings each payday."
        ]
        if df is not None:
            cat_sums = df.groupby("category_clean")["expense"].sum().sort_values(ascending=False)
            if len(cat_sums) > 0:
                top = cat_sums.index[0]
                tips.insert(0, f"You spend most on '{top}'. Consider a spending cap or alternative cheaper choices for this category.")
        reply = "Suggestions:\n• " + "\n• ".join(tips)
    
    elif "prediction" in msg or "forecast" in msg:
        if df is None:
            reply = "Upload your CSV data to get expense predictions."
        else:
            try:
                df_pred = df.copy()
                df_pred['date'] = pd.to_datetime(df_pred[meta['date_col']])
                df_pred['amount'] = df_pred['expense']
                monthly_totals = aggregate_past_months(df_pred)
                predicted_next = predict_next_total(monthly_totals)
                reply = f"Predicted spending for next month: ₹{predicted_next:.2f}"
            except Exception as e:
                reply = f"Could not generate prediction: {str(e)}"
    
    elif "hello" in msg or "hi" in msg or "hey" in msg:
        reply = "Hi! I'm SpendGenie AI. Ask me about 'top categories', 'monthly trend', 'predictions', or say 'reduce dining' to get tips."
    
    elif "help" in msg:
        reply = "I can help with:\n• Analyzing your spending patterns\n• Predicting future expenses\n• Budgeting tips\n• Understanding your top categories\nTry asking: 'What are my top categories?' or 'How can I save money?'"
    
    else:
        if "dining" in msg or "food" in msg or "restaurants" in msg:
            reply = "Dining tips: set a weekly limit, prefer home-cooked meals, and track small purchases — they add up."
        elif "subscription" in msg or "subscriptions" in msg:
            reply = "Check your recurring charges: map them and cancel ones you rarely use."
        elif "budget" in msg:
            reply = "Budgeting tip: Use the 50/30/20 rule - 50% needs, 30% wants, 20% savings."
        else:
            if df is not None:
                total = df["expense"].sum()
                reply = f"I analyzed your data: total recorded spending: ₹{total:,.2f}. Ask 'top categories' or 'monthly trend' for more details."
            else:
                reply = "I can provide budget tips and analyze uploaded CSVs. Upload a CSV to get personalized suggestions."
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧞 SPENDGENIE BACKEND - Starting Server")
    print("="*60)
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"📁 Backend Directory: {BACKEND_DIR}")
    print(f"📁 Data Directory: {BASE_DIR}")
    print(f"💾 Database: {DB_PATH}")
    print(f"🌐 Server: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
