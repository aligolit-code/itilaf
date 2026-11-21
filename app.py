import streamlit as st
import os

st.set_page_config(page_title="منصة باحثي الائتلاف السوداني", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@900&display=swap" rel="stylesheet">
<style>
.main-title {
    font-family: 'Amiri', 'Cairo', serif;
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700, #00B894);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.4;
    margin-top: 5px;
    margin-bottom: 5px;
}
.sub-title {
    font-family: 'Cairo', sans-serif;
    text-align: center;
    color: #666;
    font-size: 16px;
    margin-top: 0px;
}
</style>
""", unsafe_allow_html=True)

for f in os.listdir("."):
    if f.startswith("Screenshot") and f.endswith((".jpg", ".png", ".jpeg")):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(f, width=150)
        break

st.markdown('<div class="main-title">✦ منصة باحثي الائتلاف السوداني ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">الأوراق العلمية، والفرص البحثية في مكان واحد</div>', unsafe_allow_html=True)
st.markdown("---")

researchers = {
    "مكارم": "makarem123",
    "ثويبة": "thawiba123",
    "فكتوريا": "victoria123",
    "علي": "ali123",
    "هديل": "hadeel123",
    "هناء": "hanaa123",
    "سعاد": "suad123",
    "صالح": "saleh123",
    "نشوى": "nashwa123",
    "مستر ناجي": "nagi123",
    "دكتورة نادية": "nadia123",
    "رحاب": "rehab123",
    "سليمى": "salma123",
    "معاذ": "moaz123",
}

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
</style>
""", unsafe_allow_html=True
