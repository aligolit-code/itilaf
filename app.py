from flask import Flask, render_template_string, request, redirect, session
import json, os, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "itilaf-secret-2026"
DATA_FILE = "data.json"
ADMINS = ["aligolit15"]

def load():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "posts": []}
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

LOGIN_HTML = """<html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>الائتلاف</title><style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px;text-align:center}h1{font-size:22px}.sub{color:#b7c9c0;font-size:14px;margin-bottom:20px}.card{background:#fff;color:#222;border-radius:18px;padding:20px;text-align:right}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-top:6px;margin-bottom:12px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold;cursor:pointer}.msg{background:#ffe4e4;color:#b91c1c;padding:10px;border-radius:10px;margin-bottom:10px;text-align:center}.ok{background:#dcfce7;color:#166534;padding:10px;border-radius:10px;margin-bottom:10px;text-align:center}a{color:#16a34a;display:block;text-align:center;margin-top:15px;text-decoration:none;font-weight:bold}</style></head><body><div class="box"><h1>الائتلاف السوداني</h1><div class="sub">منصة الباحثين السودانيين</div><div class="card">{MSG}<form method="post"><label>اسم المستخدم</label><input name="username" required><label>كلمة السر</label><input type="password" name="password" required><button class="btn">دخول</button></form><a href="/register">ما عندك حساب؟ سجل جديد</a></div></div></body></html>"""

@app.route("/", methods=["GET","POST"])
def login():
    msg = ""
    if request.method == "POST":
        data = load()
        u = request.form.get("username","").strip()
        p = hash_pw(request.form.get("password",""))
        found = None
        for x in data["users"]:
            if x["username"] == u and x["password"] == p:
                found = x
        if found is None:
            msg = "<div class='msg'>اسم المستخدم او كلمة السر غلط</div>"
        elif found.get("status") != "approved":
            msg = "<div class='msg'>حسابك لسه قيد المراجعة</div>"
        else:
            session["user"] = u
            return redirect("/home")
    ok = request.args.get("ok","")
    if ok:
        msg = "<div class='ok'>" + ok + "</div>" + msg
    html = LOGIN_HTML.replace("{MSG}", msg)
    return html

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = load()
        u = request.form.get("username","").strip()
        exists = False
        for x in data["users"]:
            if x["username"] == u:
                exists = True
        if exists:
            return "الاسم ده مسجل قبل كده <a href='/register'>رجوع</a>"
        new_user = {}
        new_user["username"] = u
        new_user["name"] = request.form.get("name","")
        new_user["password"] = hash_pw(request.form.get("password",""))
        new_user["status"] = "pending"
        new_user["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        data["users"].append(new_user)
        save(data)
        return redirect("/?ok=تم التسجيل بنجاح، انتظر الموافقة")
    return """<html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px}.card{background:#fff;color:#222;border-radius:18px;padding:20px}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;margin-bottom:10px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-weight:bold}a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}</style></head><body><div class="box"><h2 style="text-align:center">تسجيل عضو جديد</h2><div class="card"><form method="post"><input name="username" placeholder="اسم المستخدم" required><input name="name" placeholder="الاسم الكامل" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">تسجيل</button></form><a href="/">رجوع للدخول</a></div></div></body></html>"""

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    data = load()
    me = None
    for x in data["users"]:
        if x["username"] == session["user"]:
            me = x
    is_admin = session.get("user") in ADMINS
    html = "<h2 style='text-align:center;font-family:Tahoma'>اهلا
