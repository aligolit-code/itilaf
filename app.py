from flask import Flask, request, redirect, session, send_file
import json, os, hashlib
from datetime import datetime

app = Flask(__name__)

@app.route("/manifest.json")
def manifest():
    return send_file("manifest.json", mimetype="application/json")
@app.route("/icon-192.png")
def icon192():
    return send_file("icon-192.png", mimetype="image/png")
@app.route("/icon-512.png")
def icon512():
    return send_file("icon-512.png", mimetype="image/png")

@app.after_request
def add_manifest(response):
    if 'text/html' in response.content_type:
        data = response.get_data(as_text=True).replace('</head>', "<link rel='manifest' href='/manifest.json'></head>", 1)
        response.set_data(data)
    return response

app.secret_key = os.environ.get("SECRET_KEY", "itilaf-secret-2026")
DATA_FILE = os.environ.get("DATA_FILE", "data.json")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
ADMINS = ["aligolit15", "aburazan"]

# ---------- قاعدة البيانات الثابتة ----------
def _pg_conn():
    import psycopg2
    url = DATABASE_URL
    # Render بيدي postgres:// ولازم تبقى postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url)

def _pg_init():
    try:
        conn = _pg_conn()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, name TEXT, password TEXT, status TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS posts (id SERIAL PRIMARY KEY, username TEXT, text TEXT, time TEXT)")
        conn.commit()
        cur.close(); conn.close()
    except Exception as e:
        print("PG init error:", e)

def _use_pg():
    return bool(DATABASE_URL)

if _use_pg():
    _pg_init()

def load():
    if _use_pg():
        try:
            conn = _pg_conn()
            cur = conn.cursor()
            cur.execute("SELECT username, name, password, status FROM users")
            users = [{"username": r[0], "name": r[1], "password": r[2], "status": r[3]} for r in cur.fetchall()]
            cur.execute("SELECT username, text, time FROM posts ORDER BY id ASC")
            posts = [{"user": r[0], "text": r[1], "time": r[2]} for r in cur.fetchall()]
            cur.close(); conn.close()
            return {"users": users, "posts": posts}
        except Exception as e:
            print("PG load error:", e)
            return {"users": [], "posts": []}
    if not os.path.exists(DATA_FILE):
        return {"users": [], "posts": []}
    with open(DATA_FILE, encoding="utf-8") as f:
        d = json.load(f)
        if "posts" not in d: d["posts"] = []
        return d

def save(data):
    if _use_pg():
        try:
            conn = _pg_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM users")
            for u in data["users"]:
                cur.execute("INSERT INTO users (username, name, password, status) VALUES (%s,%s,%s,%s) ON CONFLICT (username) DO UPDATE SET name=EXCLUDED.name, password=EXCLUDED.password, status=EXCLUDED.status",
                            (u["username"], u.get("name",""), u.get("password",""), u.get("status","approved")))
            cur.execute("DELETE FROM posts")
            for p in data["posts"]:
                cur.execute("INSERT INTO posts (username, text, time) VALUES (%s,%s,%s)",
                            (p["user"], p["text"], p["time"]))
            conn.commit()
            cur.close(); conn.close()
            return
        except Exception as e:
            print("PG save error:", e)
            return
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

LOGIN_PAGE = """
<html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>الائتلاف</title>
<style>body{margin:0;background:#0f1f1a;color:#fff}.box{max-width:420px;margin:auto;padding:20px;text-align:center}.card{background:#fff;color:#222;border-radius:18px;padding:20px}input{width:100%;padding:13px;border-radius:10px;margin-bottom:12px}.btn{width:100%;background:#16a34a;color:#fff;padding:14px;border-radius:12px}.msg{background:#ffe4e4;padding:10px;border-radius:10px}.ok{background:#dcfce7;padding:10px;border-radius:10px}</style></head>
<body><div class="box"><h1>الائتلاف السوداني للتعليم للجميع</h1><p>منتدى الباحثين</p><div class="card">__MSG__
<form method="post"><input name="username" placeholder="اسم المستخدم" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">دخول</button></form>
<a href="/register">ما عندك حساب؟ سجل جديد</a></div></div></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        data = load()
        u = request.form.get("username", "").strip()
        p = hash_pw(request.form.get("password", ""))
        found = None
        for x in data["users"]:
            if x["username"] == u and x["password"] == p:
                found = x
        if found is None:
            msg = "<div class='msg'>غلط في الاسم او كلمة السر</div>"
        elif found.get("status") != "approved":
            msg = "<div class='msg'>حسابك لسه قيد المراجعة</div>"
        else:
            session["user"] = u
            return redirect("/home")
    ok = request.args.get("ok", "")
    if ok:
        msg = "<div class='ok'>" + ok + "</div>" + msg
    return LOGIN_PAGE.replace("__MSG__", msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = load()
        u = request.form.get("username", "").strip()
        for x in data["users"]:
            if x["username"] == u:
                return "الاسم مسجل قبل كده"
        new_user = {"username": u, "name": request.form.get("name", ""), "password": hash_pw(request.form.get("password", "")), "status": "approved"}
        data["users"].append(new_user)
        save(data)
        return redirect("/?ok=تم التسجيل بنجاح")
    return """<html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:#0f1f1a;color:#fff;text-align:center"><h2>تسجيل عضو جديد</h2><form method="post"><input name="username" placeholder="اسم المستخدم" required><br><br><input name="name" placeholder="الاسم الكامل" required><br><br><input type="password" name="password" placeholder="كلمة السر" required><br><br><button>تسجيل</button></form><a href="/">رجوع</a></body></html>"""

@app.route("/home")
def home():
    if "user" not in session: return redirect("/")
    data = load()
    me = next((x for x in data["users"] if x["username"] == session["user"]), {"name": session["user"]})
    out = """<html lang='ar' dir='rtl'><head><meta name='viewport' content='width=device-width, initial-scale=1.0'><style>
    body{{margin:0;background:#0f1f1a;color:#fff;font-family:sans-serif;text-align:center}}
    .box{{max-width:500px;margin:auto;padding:20px}}
    .card{{background:#fff;color:#222;border-radius:20px;padding:22px;margin-top:15px;text-align:right}}
    .btn{{display:block;background:#16a34a;color:#fff;padding:18px;border-radius:14px;text-decoration:none;font-size:22px;font-weight:bold;text-align:center}}
    .member{{background:#1e3a2f;padding:16px;border-radius:14px;margin:10px 0;font-size:20px}}
    .member a{{color:#fff;text-decoration:none;font-size:20px}}
    h2{{font-size:28px}} h3{{font-size:22px}}
    </style></head><body><div class='box'><h2>اهلا {me['name']} 👋</h2>
    <a href='/forum' class='btn'>💬
"""
    return out
