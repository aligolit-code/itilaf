import streamlit as st
import os

st.set_page_config(page_title="منصة الباحثين", layout="centered")

# الشعار - بفتش الصورة براهو
for f in os.listdir("."):
    if f.startswith("Screenshot") and f.endswith((".jpg", ".png", ".jpeg")):
        st.image(f, use_container_width=True)
        break

st.markdown("<h1 style='text-align:center'>باحثين الائتلاف السوداني</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center'>منصة تجمع الباحثين السودانيين</h3>", unsafe_allow_html=True)
st.markdown("---")
st.write("الأوراق العلمية، والفرص البحثية في مكان واحد.")

# الباحثين والباسويردات
researchers = {
    "مكارم": "makarem123",
    "ثوية": "thawya123",
    "فكتوريا": "victoria123",
    "علي": "ali123",
    "هديل": "hadeel123",
    "هناء": "hanaa123",
    "سعاد": "suad123",
    "صالح": "saleh123",
    "نشوى": "nashwa123",
    "مستر ناجي": "nagi123",
    "دكتورة نادية": "nadia123",
}

# الستايل الأصفر المنور - نفس الصيغة القديمة
st.markdown("""
<style>
.stButton > button {
    background: linear-gradient(45deg, #FFD700, #FFEA00);
    color: #000;
    font-size: 20px;
    font-weight: bold;
    border-radius: 20px;
    border: 2px solid #FFC400;
    box-shadow: 0 0 20px #FFD700;
    width: 100%;
    padding: 15px;
    margin: 5px 0px;
}
.stButton > button:hover {
    box-shadow: 0 0 30px #FFD700;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📚 أضف بحثك", "👥 الباحثون", "📄 الأبحاث"])

with tab1:
    st.subheader("أضف بحثك")
    st.write("ارفع بحثك هنا وشاركو مع باقي الباحثين.")

with tab2:
    st.subheader("الباحثون")
    st.write("قائمة الباحثين المسجلين في ائتلاف:")
    st.write("اضغط على اسمك واكتب كلمة سرك لتدخل ملفك ✨")

    for name, password in researchers.items():
        if st.button(f"✨ {name} ✨", key=f"btn_{name}"):
            st.session_state["selected"] = name

    if "selected" in st.session_state:
        name = st.session_state["selected"]
        st.markdown(f"### مرحباً {name} 👋")
        pw = st.text_input("اكتب كلمة سرك", type="password", key=f"pw_{name}")
        if st.button("ادخل مكان النقاش", key=f"enter_{name}"):
            if pw == researchers[name]:
                st.success(f"أهلاً بيك {name}، دخلت ملفك ✅")
                st.write(f"هنا ملف {name} الخاص - مكان النقاش والبحوث.")
            elif pw == "":
                st.warning("اكتب كلمة سرك أولاً")
            else:
                st.error("كلمة السر غلط، حاول تاني")

with tab3:
    st.subheader("الأبحاث")
    st.write("قريباً: أحدث الأوراق والأبحاث المنشورة")
