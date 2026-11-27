from flask import Flask, request, redirect, session
import json, os, hashlib
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'itilaf-secret-2026'
DATA_FILE = 'data.json'
ADMINS = ['aligolit15']
def load():
    if not os.path.exists(DATA_FILE):
        return {'users': [{'username': 'aligolit15', 'name': 'علي', 'password': hashlib.sha256('123456'.encode()).hexdigest(), 'status': 'approved'}], 'messages': []}
    with open(DATA_FILE, encoding='utf-8') as f:
        d = json.load(f)
        if 'messages' not in d:
            d['messages'] = []
        if 'users' not in d:
            d['users'] = []
        return d
def save(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()
def login_page(msg=''):
    m = ''
    if msg:
        m = '<div style="background:#ffe4e4;padding:10px;border-radius:10px;text-align:center">' + msg + '</div>'
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>الائتلاف</title><style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px;text-align:center}.card{background:#fff;color:#222;border-radius:18px;padding:20px;text-align:right}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-bottom:10px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold}a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}</style></head><body><div class="box"><h1>الائتلاف السوداني</h1><p>منصة الباحثين السودانيين</p><div class="card">' + m + '<form method="post"><input name="username" placeholder="اسم المستخدم" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">دخول</button></form><a href="/register">ما عندك حساب؟ سجل جديد</a></div></div></body></html>'
def register_page():
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>تسجيل</title><style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#0f1f1a;color:#fff;display:flex;justify-content:center}.box{width:100%;max-width:420px;padding:20px}.card{background:#fff;color:#222;border-radius:18px;padding:20px}input{width:100%;padding:13px;border:1px solid #ccc;border-radius:10px;font-size:16px;margin-bottom:10px}.btn{width:100%;background:#16a34a;color:#fff;border:none;padding:14px;border-radius:12px;font-size:17px;font-weight:bold}a{color:#16a34a;display:block;text-align:center;margin-top:12px;text-decoration:none;font-weight:bold}</style></head><body><div class="box"><h2 style="text-align:center">تسجيل عضو جديد</h2><div class="card"><form method="post"><input name="username" placeholder="اسم المستخدم" required><input name="name" placeholder="الاسم الكامل" required><input type="password" name="password" placeholder="كلمة السر" required><button class="btn">تسجيل</button></form><a href="/">رجوع للدخول</a></div></div></body></html>'
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = load()
        u = request.form.get('username', '').strip()
        p = hash_pw(request.form.get('password', ''))
        user = None
        for x in data['users']:
            if x['username'] == u and x['password'] == p:
                user = x
        if not user:
            return login_page('اسم المستخدم أو كلمة السر غلط')
        if user.get('status') != 'approved':
            return login_page('حسابك لسه قيد المراجعة، انتظر موافقة المشرف')
        session['user'] = u
        return redirect('/home')
    ok = request.args.get('ok', '')
    return login_page(ok)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = load()
        u = request.form.get('username', '').strip()
        for x in data['users']:
            if x['username'] == u:
                return 'الاسم ده مسجل قبل كده <a href="/register">رجوع</a>'
        data['users'].append({'username': u, 'name': request.form.get('name', ''), 'password': hash_pw(request.form.get('password', '')), 'status': 'pending'})
        save(data)
        return redirect('/?ok=تم التسجيل بنجاح، انتظر الموافقة')
    return register_page()
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    data = load()
    me = None
    for x in data['users']:
        if x['username'] == session['user']:
            me = x
    if not me:
        session.clear()
        return redirect('/')
    my_name = me['name']
    is_admin = session['user'] in ADMINS
    pending = []
    if is_admin:
        for x in data['users']:
            if x.get('status') == 'pending':
                pending.append(x)
    approved_users = []
    for x in data['users']:
        if x.get('status') == 'approved':
            approved_users.append(x)
    messages = data.get('messages', [])
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"><title>غرفة النقاش</title><style>*{box-sizing:border-box;font-family:Tahoma}body{margin:0;background:#eef2f0;padding:0}.top{background:#0f1f1a;color:#fff;padding:16px;text-align:center;position:sticky;top:0;z-index:10}.top h2{margin:0;font-size:22px}.top p{margin:4px 0 0;color:#b7c9c0;font-size:14px}.wrap{width:100%;padding:12px;padding-bottom:90px}.card{background:#fff;border-radius:14px;padding:14px;margin-bottom:12px;font-size:16px;line-height:1.6}.pending{background:#fef9c3}.pending a{display:inline-block;background:#fff;padding:6px 12px;border-radius:8px;margin:4px;text-decoration:none;font-weight:bold}.chat{min-height:55vh}.msg{margin:10px 0;padding:10px 12px;background:#f1f5f3;border-radius:12px;font-size:17px}.msg small{color:#888;font-size:12px}.sendbar{position:fixed;bottom:0;left:0;right:0;background:#fff;padding:10px;display:flex;gap:8px;border-top:1px solid #ddd;z-index:20}.sendbar input{flex:1;padding:15px;border:1px solid #ccc;border-radius:25px;font-size:17px;outline:none}.sendbar button{background:#16a34a;color:#fff;border:none;padding:0 22px;border-radius:25px;font-size:17px;font-weight:bold}.logout{display:block;text-align:center;margin-top:10px;color:#666}</style></head><body>'
    html += '<div class="top"><h2>اهلا ' + my_name + '</h2><p>غرفة نقاش الائتلاف</p></div>'
    html += '<div class="wrap">'
    if is_admin and len(pending) > 0:
        html += '<div class="card pending"><b>طلبات قيد الانتظار (' + str(len(pending)) + ')</b><br>'
        for p in pending:
            html += '<div>' + p['name'] + ' - @' + p['username'] + ' <a href="/approve/' + p['username'] + '">موافقة</a> <a href="/reject/' + p['username'] + '">رفض</a></div>'
        html += '</div>'
    html += '<div class="card"><b>الاعضاء (' + str(len(approved_users)) + ')</b><br>'
    for u in approved_users:
        html += '• ' + u['name'] + ' @' + u['username'] + '<br>'
    html += '</div>'
    html += '<div class="card chat"><b>غرفة النقاش</b><hr>'
    if len(messages) == 0:
        html += '<p style="color:#888;text-align:center">لسه ما في رسائل، كن أول زول يكتب</p>'
    for m in messages[-100:]:
        html += '<div class="msg"><b>' + m.get('name', '') + ':</b> ' + m.get('text', '') + '<br><small>' + m.get('time', '') + '</small></div>'
    html += '</div><a class="logout" href="/logout">خروج</a></div>'
    html += '<form class="sendbar" method="post" action="/send"><input name="text" placeholder="اكتب رسالتك هنا..." required><button>إرسال</button></form></body></html>'
    return html
@app.route('/send', methods=['POST'])
def send():
    if 'user' not in session:
        return redirect('/')
    data = load()
    me = None
    for x in data['users']:
        if x['username'] == session['user']:
            me = x
    text = request.form.get('text', '').strip()
    if text and me:
        data['messages'].append({'name': me['name'], 'username': me['username'], 'text': text, 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
        save(data)
    return redirect('/home')
@app.route('/approve/<username>')
def approve(username):
    if session.get('user') not in ADMINS:
        return 'ما عندك صلاحية'
    data = load()
    for u in data['users']:
        if u['username'] == username:
            u['status'] = 'approved'
    save(data)
    return redirect('/home')
@app.route('/reject/<username>')
def reject(username):
    if session.get('user') not in ADMINS:
        return 'ما عندك صلاحية'
    data = load()
    new_users = []
    for u in data['users']:
        if u['username'] != username:
            new_users.append(u)
    data['users'] = new_users
    save(data)
    return redirect('/home')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
