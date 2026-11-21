import streamlit as st
import os
st.set_page_config(
    page_title='منصة باحثي الائتلاف السوداني',
    layout='centered'
)
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@900&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)
css = '.main-title{font-family:Amiri,Cairo,serif;'
css = css + 'font-size:38px;font-weight:700;'
css = css + 'text-align:center;'
css = css + 'background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700,#00B894);'
css = css + '-webkit-background-clip:text;'
css = css + '-webkit-text-fill-color:transparent;}'
css = css + '.sub-title{font-family:Cairo,sans-serif;'
css = css + 'text-align:center;color:#666;font-size:16px;}'
css = css + '.stButton>button{background:linear-gradient(45deg,#FFD700,#FFEA00);'
css = css + 'color:#000;font-size:20px;font-weight:bold;'
css = css + 'border-radius:20px;border:2px solid #FFC400;'
css = css + 'box-shadow:0 0 20px #FFD700;width:100%;padding:15px;}'
st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)
for f in os.listdir('.'):
    if f.startswith('Screenshot'):
        if f.endswith('.jpg') or f.endswith('.png'):
            st.image(f, use_container_width=True)
            break
st.markdown('<div class="main-title">منصة باحثي الائتلاف السوداني</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">الاوراق العلمية، والفرص البحثية في مكان واحد</div>', unsafe_allow_html=True)
st.markdown('---')
researchers = []
researchers.append('مستر ناجي')
researchers.append('دكتورة نادية')
researchers.append('نشوى')
researchers.append('مكارم')
researchers.append('ثويبة')
researchers.append('فكتوريا')
researchers.append('علي')
researchers.append('هديل')
researchers.append('هناء')
researchers.append('سعاد')
researchers.append('صالح')
researchers.append('رحاب')
researchers.append('سليمى')
researchers.append('معاذ')
researchers.append('أمنة')
tab1, tab2, tab3 = st.tabs(['اضف بحثك', 'الباحثون', 'الابحاث'])
with tab1:
    st.subheader('اضف بحثك')
    st.write('ارفع بحثك هنا وشاركو مع باقي الباحثين.')
with tab2:
    st.subheader('الباحثون')
    st.write('اضغط على اسمك واكتب طوالي')
    for name in researchers:
        if st.button(name, key='btn_' + name):
            st.session_state['selected'] = name
    if 'selected' in st.session_state:
        name = st.session_state['selected']
        st.markdown('### مرحبا ' + name)
        st.markdown('### مكان النقاش الخاص بـ ' + name)
        new_msg = st.text_area('اكتب رسالتك هنا...', key='msg_' + name)
        if st.button('انشر رسالتي', key='send_' + name):
            if new_msg.strip() != '':
                key_chat = 'chat_' + name
                if key_chat not in st.session_state:
                    st.session_state[key_chat] = []
                st.session_state[key_chat].append(new_msg)
                st.success('اتنشرت رسالتك')
            else:
                st.warning('اكتب حاجة اولا')
        st.markdown('---')
        st.write('رسائلك المنشورة:')
        key_chat = 'chat_' + name
        if key_chat in st.session_state:
            if len(st.session_state[key_chat]) > 0:
                for m in reversed(st.session_state[key_chat]):
                    st.info(m)
            else:
                st.write('لسه ما كتبت حاجة')
        else:
            st.write('لسه ما كتبت حاجة')
with tab3:
    st.subheader('الابحاث')
    st.write('قريبا: احدث الاوراق والابحاث المنشورة')
