import streamlit as st
import os
st.set_page_config(page_title='منصة باحثي الائتلاف السوداني', layout='centered')
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@900&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown('<style>.main-title{font-family:Amiri,Cairo,serif;font-size:38px;font-weight:700;text-align:center;background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700,#00B894);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.4;margin-top:5px;margin-bottom:5px;}.sub-title{font-family:Cairo,sans-serif;text-align:center;color:#666;font-size:16px;margin-top:0px;}.stButton>button{background:linear-gradient(45deg,#FFD700,#FFEA00);color:#000;font-size:20px;font-weight:bold;border-radius:20px;border:2px solid #FFC400;box-shadow:0 0 20px #FFD700;width:100%;padding:15px;margin:5px 0px;}</style>', unsafe_allow_html=True)
for f in os.listdir('.'):
    if f.startswith('Screenshot') and f.endswith(('.jpg','.png','.jpeg')):
        st.image(f, use_container_width=True)
        break
st.markdown('<div class="main-title">منصة باحثي الائتلاف السوداني</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">الاوراق العلمية، والفرص البحثية في مكان واحد</div>', unsafe_allow_html=True)
st.markdown('---')
researchers=['مستر ناجي','دكتورة نادية','نشوى','مكارم','ثويبة','فكتوريا','علي','هديل','هناء','سعاد','صالح','رحاب','سليمى','معاذ','أمنة']
tab1,tab2,tab3=st.tabs(['اضف بحثك','الباحثون','الابحاث'])
with tab1:
    st.subheader('اضف بحثك')
    st.write('ارفع بحثك هنا وشاركو مع باقي الباحثين.')
with tab2:
    st.subheader('الباحثون')
    st.write('اضغط على اسمك واكتب طوالي')
    for name in researchers:
        if st.button(f'{name}', key=f'btn
