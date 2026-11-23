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
        "chats": [], "papers": [], "posts": []
    }

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

# الغلاف - الشعار مستطيل زي ما هو
st.image("Screenshot_20261120_230914_com_whatsapp_ViewProfilePhoto.jpg", use_container_width=True)

st.markdown("""
<div style="text-align:center; padding:20px 10px; background:#14532d; border-radius:20px; border:3px solid #22c55e;">
    <div style="font-size:32px; font-weight:900; color:#ffffff; white-space:nowrap; text-shadow:2px 2px 0px #dc2626;">
        باحثي الائتلاف السوداني
    </div>
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

tab1, tab2, tab3, tab4 = st.tabs(["📝 المنتدى", "👤 صفحتي", "👥 الأعضاء", "📚 الأبحاث"])
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
    # لو فاتح منشور معين - اظهر زر الرجوع
    if "opened_post" in st.session_state and st.session_state["opened_post"] is not None:
        pid = st.session_state["opened_post"]
        p = next((x for x in data["posts"] if x["id"] == pid), None)
        if st.button("⬅️ رجوع للمنتدى"):
            st.session_state["opened_post"] = None
            st.rerun()
        if p:
            st.subheader(f"[{p['cat']}] {p['title']}")
            st.write(f"بواسطة: {p['name']}")
            st.markdown("---")
            st.write(p["text"])
            st.markdown("---")
            st.markdown("**التعليقات:**")
            for c in p.get("comments", []):
                st.info(f"{c['name']} : {c['text']}")
            new_c = st.text_input("اكتب تعليق...", key=f"c_{p['id']}")
            if st.button("علق"):
                if new_c.strip():
                    p.setdefault("comments", []).append({"name": me["name"], "user": st.session_state["user"], "text": new_c})
                    save_data(data); st.rerun()
            if p["user"] == st.session_state["user"] or me["role"] == "admin":
                if st.button("حذف المنشور"):
                    data["posts"] = [x for x in data["posts"] if x["id"] != p["id"]]
                    st.session_state["opened_post"] = None
                    save_data(data); st.rerun()
        st.stop()

    # لو ما فاتح منشور - اظهر قائمة المنتدى
    st.subheader("المنتدى - منشورات الأعضاء")
    cats = ["بحوث ودراسات", "نقاش عام", "فرص ومنح", "أسئلة ومساعدة"]
    cat = st.selectbox("اختار القسم", cats)
    p_title = st.text_input("عنوان المنشور")
    p_text = st.text_area("اكتب منشورك هنا...", key="post_text")
    if st.button("انشر المنشور"):
        if p_title.strip() and p_text.strip():
            data["posts"].append({"id": len(data["posts"])+1, "title": p_title, "text": p_text, "cat": cat, "name": me["name"], "user": st.session_state["user"], "comments": []})
            save_data(data); st.success("اتنشر"); st.rerun()
        else:
            st.warning("اكتب العنوان والنص")

    st.markdown("---")
    f_cat = st.selectbox("اعرض قسم:", ["الكل"] + cats)
    for p in reversed(data["posts"]):
        if f_cat != "الكل" and p["cat"] != f_cat:
            continue
        st.info(f"[{p['cat']}] {p['title']} - بواسطة {p['name']} - {len(p.get('comments',[]))} تعليق")
        if st.button(f"افتح المنشور", key=f"open_{p['id']}"):
            st.session_state["opened_post"] = p["id"]
            st.rerun()
with tab2:
    st.subheader("صفحتي - اتحكم في ملفك براك")
    me["name"] = st.text_input("اسمك الكامل", value=me["name"])
    me["specialty"] = st.text_input("تخصصي", value=me["specialty"])
    me["bio"] = st.text_area("نبذتي", value=me["bio"])
    me["email"] = st.text_input("ايميلي", value=me["email"])
    new_pw = st.text_input("كلمة سر جديدة (خليها فاضية لو ما داير تغيرها)", type="password")
    if st.button("حفظ ملفي"):
        if new_pw.strip():
            me["pw"] = hash_pw(new_pw)
        save_data(data); st.success("تم حفظ ملفك")

    st.markdown("---")
    st.subheader("منشوراتي أنا")
    my_posts = [x for x in data["posts"] if x["user"] == st.session_state["user"]]
    if not my_posts:
        st.write("لسه ما نشرت أي منشور")
    for p in reversed(my_posts):
        st.write(f"**[{p['cat']}] {p['title']}** - {len(p.get('comments',[]))} تعليق")
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
