from flask import Flask
from flask import request
from flask import redirect
from flask import session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "itilaf-secret-2026"
DATA_FILE = "data.json"
ADMINS = ["aligolit15", "aburazan"]

def load():
    if not os.path.exists(DATA_FILE):
        return {"users": []}
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

LOGIN_PAGE = """
<html lang="ar" dir="rtl">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الائتلاف</title>
<style>
body{margin:0;background:#0f1f1a;color:#fff}
.box{max-width:420px;margin:auto;padding:20px;text-align:center}
.card{background:#fff;color:#222;border-radius:18px;padding:20px}
input{width:100%;padding:13px;border-radius:10px;margin-bottom:12px}
.btn{width:100%;background:#16a34a;color:#fff;padding:14px;border-radius:12px}
.msg{background:#ffe4e4;padding:10px;border-radius:10px}
.ok{background:#dcfce7;padding:10px;border-radius:10px}
</style>
</head>
<body>
<div class="box">
<h1>الائتلاف السوداني للتعليم للجميع</h1>
<p>منتدى الباحثين</p>

<div class="card">
__MSG__
<form method="post">
<input name="username" placeholder="اسم المستخدم" required>
<input type="password" name="password" placeholder="كلمة السر" required>
<button class="btn">دخول</button>
</form>
<a href="/register">ما عندك حساب؟ سجل جديد</a>
</div>
</div>
</body>
</html>
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
            if x["username"] == u:
                if x["password"] == p:
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
    page = LOGIN_PAGE.replace("__MSG__", msg)
    return page

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = load()
        u = request.form.get("username", "").strip()
        for x in data["users"]:
            if x["username"] == u:
                return "الاسم مسجل قبل كده"
        new_user = {}
        new_user["username"] = u
        new_user["name"] = request.form.get("name", "")
        new_user["password"] = hash_pw(request.form.get("password", ""))
        new_user["status"] = "approved"
        data["users"].append(new_user)
        save(data)
        return redirect("/?ok=تم التسجيل، انتظر الموافقة")
    return """
<html lang="ar" dir="rtl">
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background:#0f1f1a;color:#fff;text-align:center">
<h2>تسجيل عضو جديد</h2>
<form method="post">
<input name="username" placeholder="اسم المستخدم" required><br><br>
<input name="name" placeholder="الاسم الكامل" required><br><br>
<input type="password" name="password" placeholder="كلمة السر" required><br><br>
<button>تسجيل</button>
</form>
<a href="/">رجوع</a>
</body>
</html>
"""

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    data = load()
    me = None
    for x in data["users"]:
        if x["username"] == session["user"]:
            me = x
    out = "<h2>اهلا " + me["name"] + "</h2>"
    if session.get("user") in ADMINS:
        out = out + "<h3>طلبات قيد الانتظار</h3>"
        for p in data["users"]:
            if p.get("status") == "pending":
                out = out + "<div>"
                out = out + p["name"]
                out = out + " @"
                out = out + p["username"]
                out = out + " <a href='/approve/"
                out = out + p["username"]
                out = out + "'>موافقة</a> | <a href='/reject/"
                out = out + p["username"]
                out = out + "'>رفض</a></div>"
    out = out + "<br><a href='/logout'>خروج</a>"
    return out

@app.route("/approve/<username>")
def approve(username):
    if session.get("user") not in ADMINS:
        return "ما عندك صلاحية"
    data = load()
    for u in data["users"]:
        if u["username"] == username:
            u["status"] = "approved"
    save(data)
    return redirect("/home")

@app.route("/reject/<username>")
def reject(username):
    if session.get("user") not in ADMINS:
        return "ما عندك صلاحية"
    data = load()
    new_users = []
    for x in data["users"]:
        if x["username"] != username:
            new_users.append(x)
    data["users"] = new_users
    save(data)
    return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
