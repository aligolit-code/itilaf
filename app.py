from flask import Flask, render_template_string, request, redirect, session, jsonify
import json, os, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "itilaf-secret-2026"

DATA_FILE = "data.json"
ADMINS = ["aligolit15", "admin1", "admin2", "admin3", "admin4", "admin5", "admin6", "admin7", "admin8", "admin9", "admin10"] # عدل الأسماء دي بأسماء المشرفين الـ 11 الحقيقيين

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

# ============ صفحة الدخول المظبوطة ============
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الائتلاف - دخول</title>
<style>
*{box-sizing:border-box; font-family: Tahoma, Arial;}
body{margin:0; background:#0f1f1a; color:#fff; display:flex; justify-content:center; min-height:100vh;}
.box{width:100%; max-width:420px; padding:20px; text-align:center;}
.logo{width:110px; height:110px; object-fit:contain; background:#fff; border-radius:50%; padding:8px; margin:15px auto;}
h1{font-size:22px; margin:5px 0;}
.sub{color:#b7c9c0; font-size:14px; margin-bottom:20px;}
.card{background:#ffffff; color:#222; border-radius:18px; padding:20px; text-align:right;}
label{display:block; margin:12px 0 6px; font-weight:bold; font-size:14px;}
input{width:100%; padding:13px; border:1px solid #ccc; border-radius:10px; font-size:16px; direction:rtl; outline:none;}
input:focus{border-color:#16a34a;}
.btn{width:100%; background:#16a34a; color:#fff; border:none; padding:14px; border-radius:12px; font-size:17px; font-weight:bold; margin-top:18px; cursor:pointer;}
.btn:active{transform:scale(0.98);}
.msg{background:#ffe4e4; color:#b91c1c; padding:10px; border-radius:10px; margin-bottom:10px; font-size:14px; text-align:center;}
.ok{background:#dcfce7; color:#166534; padding:10px; border-radius:10px; margin-bottom:10px; font-size:14px; text-align:center;}
.link{color:#16a34a; text-align:center; display:block; margin-top:15px; text-decoration:none; font-weight:bold;}
</style>
</head>
<body>
<div class="box">
  <img class="logo" src="/static/logo.png" onerror="this.style.display='none'">
  <h1>الائتلاف السوداني</h1>
  <div class="sub">منصة الباحثين السودانيين</div>
  <div class="card">
    {% if msg %}<div class="msg">{{msg}}</div>{% endif %}
    {% if ok %}<div class="ok">{{ok}}</div>{% endif %}
    <form method="post">
      <label>اسم المستخدم</label>
      <input name="username" placeholder="مثال: aligolit15" required autocomplete="username">
      <label>كلمة السر</label>
      <input type="password" name="password" placeholder="كلمة السر" required autocomplete="current-password">
      <button class="btn">دخول</button>
    </form>
    <a class="link" href="/register">ما عندك حساب؟ سجل جديد</a>
  </div>
</div>
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تسجيل جديد</title><style>
*{box-sizing:border-box;font-family:Tahoma} body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}
.box{width:100%;max-width:420px;padding:20px}.card{background:#fff;color:#222;border-radius:18px;padding:20px}
input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-bottom:10px}
.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold;cursor:pointer}
a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}
</style></head><body><div class="box"><h2 style="text-align:center">تسجيل عضو جديد</h2>
<div class="card"><form method="post">
<input name="username" placeholder="اسم المستخدم" required>
<input name="name" placeholder="الاسم الكامل" required>
<input type="password" name="password" placeholder="كلمة السر" required>
<button class="btn">تسجيل</button></form>
<a href="/">رجوع للدخول</a></div></div></body></html>
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
            return render_template_string(LOGIN_HTML, msg="حسابك لسه قيد المراجعة، انتظر موافقة واحد من المشرفين", ok=None)
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
        data["users"].append({
            "username": u,
            "name": request.form.get("name",""),
            "password": hash_pw(request.form.get("password","")),
            "status": "pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save(data)
        return redirect("/?ok=تم التسجيل بنجاح، انتظر الموافقة من المشرفين")
    return render_template_string(REGISTER_HTML)

@app.route("/home")
def home():
    if "user" not in session: return redirect("/")
    data = load()
    me = next((x for x in data["users"] if x["username"]==session["user"]), None)
    is_admin = session["user"] in ADMINS
    pending = [x for x in data["users"] if x.get("status")=="pending"] if is_admin else []
    html = "<h2 style='text-align:center;font-family:Tahoma'>أهلا "+me["name"]+"</h2>"
    if is_admin:
        html += "<div style='max-width:500px;margin:auto;font-family:Tahoma'><h3>طلبات قيد الانتظار ("+str(len(pending))+")</h3>"
        for p in pending:
            html += f"<div style='background:#fff;color:#000;padding:12px;border-radius:10px;margin:8px 0'>{p['name']} - @{p['username']} <a href='/approve/{p['username']}'>✅ موافقة</a> | <a href='/reject/{p['username']}'>❌ رفض</a></div>"
        html += "</div>"
    html += "<div style='text-align:center'><a href='/logout'>خروج</a></div>"
    return html

@app.route("/approve/<username>")
def approve(username):
    if session.get("user") not in ADMINS: return "ما عندك صلاحية"
    data = load()
    for u in data["users"]:
        if u["username"]==username:
            u["status"]="approved"
    save(data)
    return redirect("/home")

@app.route("/reject/<username>")
def reject(username):
    if session.get("user") not in ADMINS: return "ما عندك صلاحية"
    data = load()
    data["users"] = [u for u in data["users"] if u["
