import streamlit as st

st.set_page_config(page_title="ائتلاف | منصة الباحثين", page_icon="📚", layout="wide")
st.image("Screenshot_20261120_230914_com_whatsapp_ViewProfilePhoto.jpg", width=200)
st.markdown("<h1 style='text-align:center'>ائتلاف</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center'>منصة تجمع الباحثين السودانيين</h3>", unsafe_allow_html=True)
st.markdown("---")

st.write("أهلاً بيك في ائتلاف. هنا بنجمع الباحثين، الأوراق العلمية، والفرص البحثية في مكان واحد.")

tab1, tab2, tab3 = st.tabs(["📚 الباحثون", "📄 الأبحاث", "➕ أضف بحثك"])

with tab1:
    st.subheader("الباحثون")
    st.write("قريباً: قائمة الباحثين المسجلين في ائتلاف.")

with tab2:
    st.subheader("الأبحاث")
    st.write("قريباً: أحدث الأوراق والأبحاث المنشورة.")

with tab3:
    st.subheader("أضف بحثك")
    name = st.text_input("اسمك الكامل")
    title = st.text_input("عنوان البحث")
    field = st.selectbox("مجال البحث", ["الطب", "الهندسة", "العلوم", "العلوم الاجتماعية", "أخرى"])
    if st.button("إرسال"):
        if name and title:
            st.success(f"شكراً يا {name}، تم استلام بحثك: {title}")
        else:
            st.warning("أكتب اسمك وعنوان البحث أولاً")

st.markdown("---")
st.markdown("<p style='text-align:center'>© 2026 ائتلاف - صُنع في السودان</p>", unsafe_allow_html=True)
