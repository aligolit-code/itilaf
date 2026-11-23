import streamlit as st
import os, json, hashlib

st.set_page_config(page_title="منتدى ائتلاف الباحثين", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap');
* { font-family: 'Noto Naskh Arabic', serif !important; direction: rtl; text-align: right; }
.main-title{ font-size:36px; font-weight:900; text-align:center; padding:10px; border-bottom:3px solid #FFD700; }
.stButton>button{ background:#FFD700 !important; color:#000 !important; font-size:18px; font-weight:bold; border-radius:20px; width:100%; padding:12px; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data.json"
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    # أول مرة: نعمل مشرف رئيسي - غيّر كلمة السر دي
    return {
        "users": {
            "ali_admin": {"name": "علي", "email": "ali@itilaf.com", "specialty": "إدارة المنتدى", "bio": "مشرف عام", "pw": hash_pw("123456"), "role": "admin", "status": "approved"}
        },
        "chats": [], "papers": []
    }

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

# الغلاف - الشعار مستطيل زي ما هو
st.image("logo", use_container_width=True)

st.markdown("""
<div style="
    text-align:center;
    font-size:42px;
    font-weight:900;
    line-height:1.3;
    margin-top:5px;
    margin-bottom:5px;
    background: linear-gradient(90deg, #1a237e, #0d47a1, #2e7d32);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Cairo', 'Tajawal', sans-serif;
    text-shadow: 0px 2px 10px rgba(0,0,0,0.05);
">
    ✨ منتدى باحثي الائتلاف السوداني ✨
</div>
<div style="
    text-align:center;
    font-size:18px;
    color:#666;
    margin-bottom:15px;
    letter-spacing:1px;
">
    Sudanese Coalition for Education for All • SCEFA
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# --- لو ما مسجل دخول ---
if "user" not in st.session_state:
    t1, t2 = st.tabs(["دخول", "تسجيل جديد"])
    with t1:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول"):
            if u in data["users"]:
                usr = data["users"][u]
                if usr["pw"] == hash_pw(p):
                    if usr["status"] == "pending":
                        st.warning("حسابك لسه معلق، منتظر موافقة المشرفين.")
                    elif usr["status"] == "rejected":
                        st.error("تم رفض طلبك.")
                    else:
                        st.session_state["user"] = u
                        st.rerun()
                else: st.error("كلمة السر غلط")
            else: st.error("المستخدم ما موجود")
    with t2:
        st.write("سجل حسابك، وح يتم مراجعتو من المشرفين")
        nu = st.text_input("اختار اسم مستخدم (بالانجليزي بدون مسافات)", key="nu")
        nn = st.text_input("اسمك الكامل", key="nn")
        ne = st.text_input("الإيميل", key="ne")
        ns = st.text_input("تخصصك", key="ns")
        nb = st.text_area("نبذة عنك", key="nb")
        npw = st.text_input("كلمة السر", type="password", key="npw")
        if st.button("إرسال طلب التسجيل"):
            if not nu or not nn or not npw:
                st.warning("املأ الاسم واسم المستخدم وكلمة السر")
            elif nu in data["users"]:
                st.error("اسم المستخدم ده مستخدم قبل كده، اختار واحد تاني")
            else:
                data["users"][nu] = {"name": nn, "email": ne, "specialty": ns, "bio": nb, "pw": hash_pw(npw), "role": "member", "status": "pending"}
                save_data(data)
                st.success("تم إرسال طلبك! انتظر موافقة المشرفين، وبعدها تقدر تدخل.")
    st.stop()

# --- لو مسجل دخول ---
me = data["users"][st.session_state["user"]]
st.write(f"مرحبا **{me['name']}** | تخصصك: {me['specialty']} | دورك: {'مشرف' if me['role']=='admin' else 'عضو'}")
if st.button("تسجيل خروج"):
    del st.session_state["user"]
    st.rerun()

tab1, tab2, tab3 = st.tabs(["💬 غرفة النقاش الثابتة", "👥 الأعضاء", "📚 الأبحاث"])
if me["role"] == "admin":
    tab4 = st.tabs(["✅ طلبات الانضمام"])[0]
    with tab4:
        st.subheader("طلبات جديدة")
        pending = {k:v for k,v in data["users"].items() if v["status"]=="pending"}
        if not pending: st.write("ما في طلبات جديدة")
        for k,v in pending.items():
            st.info(f"{v['name']} | {v['email']} | تخصص: {v['specialty']} | نبذة: {v['bio']}")
            c1,c2 = st.columns(2)
            if c1.button(f"قبول {v['name']}", key=f"ok_{k}"):
                data["users"][k]["status"]="approved"; save_data(data); st.rerun()
            if c2.button(f"رفض {v['name']}", key=f"no_{k}"):
                data["users"][k]["status"]="rejected"; save_data(data); st.rerun()

with tab1:
    st.markdown("### غرفة النقاش - كل الأعضاء سوا")
    new_msg = st.text_area("اكتب رسالتك هنا...", key="msg")
    if st.button("انشر رسالتي"):
        if new_msg.strip():
            data["chats"].append({"name": me["name"], "user": st.session_state["user"], "text": new_msg})
            save_data(data); st.success("اتنشرت"); st.rerun()
    st.markdown("---")
    for m in reversed(data["chats"]):
        st.info(f"{m['name']} : {m['text']}")

with tab2:
    st.subheader("ملفات الأعضاء")
    for k,v in data["users"].items():
        if v["status"]=="approved":
            with st.expander(f"{v['name']} - {v['specialty']}"):
                st.write(f"**الاسم:** {v['name']}")
                st.write(f"**التخصص:** {v['specialty']}")
                st.write(f"**النبذة:** {v['bio']}")
                st.write(f"**الإيميل:** {v['email']}")
    st.markdown("---")
    st.subheader("تعديل ملفي")
    me["specialty"] = st.text_input("تخصصي", value=me["specialty"])
    me["bio"] = st.text_area("نبذتي", value=me["bio"])
    if st.button("حفظ ملفي"):
        save_data(data); st.success("تم حفظ ملفك")

with tab3:
    st.subheader("الأبحاث")
    title = st.text_input("عنوان البحث")
    up = st.file_uploader("ارفع ملف PDF", type=["pdf"])
    if st.button("انشر البحث"):
        if title and up:
            os.makedirs("uploads", exist_ok=True)
            path = f"uploads/{title}_{st.session_state['user']}.pdf"
            with open(path, "wb") as f: f.write(up.getbuffer())
            data["papers"].append({"title": title, "author": me["name"], "file": path})
            save_data(data); st.success("اتنشر"); st.rerun()
    for p in reversed(data["papers"]):
        st.markdown(f"**{p['title']}** - بواسطة {p['author']}")
        if os.path.exists(p["file"]):
            with open(p["file"], "rb") as f:
                st.download_button(f"تحميل {p['title']}", f, file_name=os.path.basename(p["file"]), key=p["title"]+p["author"])
