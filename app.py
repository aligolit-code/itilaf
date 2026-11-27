from flask import Flask, render_template_string, request, redirect, session
import json, os, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "itilaf-secret-2026"
DATA_FILE = "data.json"
ADMINS = ["aligolit15"]

def load():
    if not os.path.exists(DATA_FILE):
        return {"users": [{"username":"aligolit15","name":"علي","password":hashlib.sha256("123456".encode()).hexdigest(),"status":"approved","created":"2026-11-27"}], "messages": []}
    with open(DATA_FILE, encoding="utf-8") as f:
        d = json.load(f)
        if "messages" not in d: d["messages"] = []
        if "users" not in d: d["users"] = []
        return d

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

LOGIN_HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>الائتلاف - دخول</title>
<style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px;text-align:center}.card{background:#fff;color:#222;border-radius:18px;padding:20px;text-align:right}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-bottom:10px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold}a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}</style>
</head><body><div class="box"><h1>الائتلاف السوداني</h1><p>منصة الباحثين السودانيين</p><div class="card">
{% if msg %}<div style="background:#ffe4e4;padding:10px;border-radius:10px;text-align:center">{{msg}}</div>{% endif %}
{% if ok %}<div style="background:#dcfce7;padding:10px;border-radius:10px;text-align:center">{{ok}}</div>{% endif %}
<form method="post"><input name="username" placeholder="اسم المستخدم" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">دخول</button></form>
<a href="/register">ما عندك حساب؟ سجل جديد</a></div></div></body></html>
"""

REGISTER_HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>تسجيل</title>
<style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px}.card{background:#fff;color:#222;border-radius:18px;padding:20px}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-bottom:10px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold}a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}</style>
</head><body><div class="box"><h2 style="text-align:center">تسجيل عضو جديد</h2><div class="card"><form method="post"><input name="username" placeholder="اسم المستخدم" required><input name="name" placeholder="الاسم الكامل" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">تسجيل</button></form><a href="/">رجوع للدخول</a></div></div></body></html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = load()
        u = request.form.get("username","").strip()
        p = hash_pw(request.form.get("password",""))
        user = next((x for x in data["users"] if x["username"]==u and x["password"]==p), None)
        if not user:
            return render_template_string(LOGIN_HTML, msg="اسم المستخدم أو كلمة السر غلط", ok=None)
        if user.get("status") != "approved":
            return render_template_string(LOGIN_HTML, msg="حسابك لسه قيد المراجعة، انتظر موافقة المشرف", ok=None)
        session["user"] = u
        return redirect("/home")
    return render_template_string(LOGIN_HTML, msg=None, ok=request.args.get("ok"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = load()
        u = request.form.get("username","").strip()
        if any(x["username"]==u for x in data["users"]):
            return "الاسم ده مسجل قبل كده <a href='/register'>رجوع</a>"
        data["users"].append({"username":u,"name":request.form.get("name",""),"password":hash_pw(request.form.get("password","")),"status":"pending","created":datetime.now().strftime("%Y-%m-%d %H:%M")})
        save(data)
        return redirect("/?ok=تم التسجيل بنجاح، انتظر الموافقة")
    return render_template_string(REGISTER_HTML)

@app.route("/home")
def home():
    if "user" not in session: return redirect("/")
    data = load()
    me = next((x for x in data["users"] if x["username"]==session["user"]), None)
    if not me:
        session.clear()
        return redirect("/")
    my_name = me["name"]
    is_admin = session["user"] in ADMINS
    pending = [x for x in data["users"] if x.get("status")=="pending"] if is_admin else []
    approved_users = [x for x in data["users"] if x.get("status")=="approved"]
    messages = data.get("messages", [])

    html = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device
