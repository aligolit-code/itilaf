from flask import Flask, request, redirect, session
import json, os, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "itilaf-secret-2026"
DATA_FILE = "data.json"
ADMINS = ["aligolit15", "aburazan"]

def load():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "posts": []}
    with open(DATA_FILE, encoding="utf-8") as f:
        d = json.load(f)
        if "posts" not in d: d["posts"] = []
        return d

def save(data):
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
    out = f"""<html lang='ar' dir='rtl'><head><meta name='viewport' content='width=device-width, initial-scale=1.0'><style>
    body{{margin:0;background:#0f1f1a;color:#fff;font-family:sans-serif;text-align:center}}
    .box{{max-width:500px;margin:auto;padding:20px}}
    .card{{background:#fff;color:#222;border-radius:20px;padding:22px;margin-top:15px;text-align:right}}
    .btn{{display:block;background:#16a34a;color:#fff;padding:18px;border-radius:14px;text-decoration:none;font-size:22px;font-weight:bold;text-align:center}}
    .member{{background:#1e3a2f;padding:16px;border-radius:14px;margin:10px 0;font-size:20px}}
    .member a{{color:#fff;text-decoration:none;font-size:20px}}
    h2{{font-size:28px}} h3{{font-size:22px}}
    </style></head><body><div class='box'><h2>اهلا {me['name']} 👋</h2>
    <a href='/forum' class='btn'>💬 غرفة النقاش العامة</a>
    <div class='card'><h3>👥 الأعضاء</h3>"""
    for u in data["users"]:
        out += f"<div class='member'><a href='/member/{u['username']}'>{u['name']} @{u['username']}</a></div>"
    out += "</div>"
    if session.get("user") in ADMINS:
        out += "<div class='card'><h3>طلبات قيد الانتظار</h3>"
        for p in data["users"]:
            if p.get("status") == "pending":
                out += f"<div>{p['name']} @{p['username']} <a href='/approve/{p['username']}'>موافقة</a> | <a href='/reject/{p['username']}'>رفض</a></div>"
        out += "</div>"
    out += "<br><a href='/logout' style='color:#fff;font-size:18px'>خروج</a></div></body></html>"
    return out

@app.route("/forum", methods=["GET", "POST"])
def forum():
    if "user" not in session: return redirect("/")
    data = load()
    if request.method == "POST":
        txt = request.form.get("text", "").strip()
        if txt:
            data["posts"].append({"user": session["user"], "text": txt, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
            save(data)
        return redirect("/forum")
    out = """<html lang='ar' dir='rtl'><head><meta name='viewport' content='width=device-width, initial-scale=1.0'><style>
    body{margin:0;background:#0f1f1a;color:#fff;font-family:sans-serif;text-align:center}
    .box{max-width:500px;margin:auto;padding:20px}
    h2{font-size:28px} input{width:100%;padding:18px;border-radius:14px;font-size:20px;box-sizing:border-box}
    .btn{background:#16a34a;color:#fff;padding:16px 30px;border-radius:12px;font-size:20px;font-weight:bold;border:none;margin-top:12px}
    .msg{background:#fff;color:#222;margin:12px 0;padding:18px;border-radius:16px;text-align:right;font-size:21px;line-height:1.6}
    .msg b{font-size:20px} .msg small{font-size:15px;color:#555}
    a{color:#fff;font-size:18px}
    </style></head><body><div class='box'><h2>غرفة النقاش العامة</h2><a href='/home'>رجوع للرئيسية</a><br><br>
    <form method='post'><input name='text' placeholder='اكتب رسالتك هنا...' required><br><button class='btn'>ارسال</button></form><hr>"""
    for p in reversed(data["posts"]):
        out += f"<div class='msg'><b><a href='/member/{p['user']}' style='color:#16a34a'>{p['user']}</a></b> <small>{p['time']}</small><br>{p['text']}</div>"
    out += "</div></body></html>"
    return out

@app.route("/member/<username>")
def member(username):
    if "user" not in session: return redirect("/")
    data = load()
    u = next((x for x in data["users"] if x["username"] == username), None)
    if not u: return "العضو غير موجود"
    out = f"<html lang='ar' dir='rtl'><body style='background:#0f1f1a;color:#fff;text-align:center;font-family:sans-serif'><h2>{u['name']}</h2><p>@{u['username']}</p><a href='/home' style='color:#fff'>رجوع</a><h3>منشوراتو</h3>"
    for p in reversed([x for x in data["posts"] if x["user"] == username]):
        out += f"<div style='background:#fff;color:#222;margin:10px;padding:12px;border-radius:12px'>{p['text']}<br><small>{p['time']}</small></div>"
    out += "</body></html>"
    return out

@app.route("/approve/<username>")
def approve(username):
    if session.get("user") not in ADMINS: return "ما عندك صلاحية"
    data = load()
    for u in data["users"]:
        if u["username"] == username: u["status"] = "approved"
    save(data)
    return redirect("/home")

@app.route("/reject/<username>")
def reject(username):
    if session.get("user") not in ADMINS: return "ما عندك صلاحية"
    data["users"] = [x for x in load()["users"] if x["username"] != username]
    save(data)
    return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
