import streamlit as st
import os, json

st.set_page_config(page_title='باحثين الائتلاف السوداني', layout='centered')

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Cairo', 'Tahoma', sans-serif !important;
    direction: rtl !important;
}
.main-title{ font-size:38px; font-weight:900; text-align:center; padding:10px; border-bottom:3px solid #FFD700; }
.stButton>button{ background:#FFD700 !important; color:#000 !important; font-size:20px; font-weight:bold; border-radius:20px; width:100%; padding:15px; }
</style>
""", unsafe_allow_html=True)

def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json','r',encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"chats": [], "papers": []}

def save_data(data):
    with open('data.json','w',encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)

if 'data' not in st.session_state: st.session_state.data = load_data()
data = st.session_state.data

st.markdown('<div class="main-title"><span style="color:#FF2D2D;">باحثين الائتلاف</span> <span style="color:#00E676;">السوداني</span></div>', unsafe_allow_html=True)
st.markdown('---')

researchers = ['مستر ناجي','دكتورة نادية','نشوى','مكارم','ثويبة','فكتوريا','علي','هديل','هناء','سعاد','صالح','رحاب','سليمى','معاذ','أمنة']

tab1, tab2 = st.tabs(['الباحثون', 'الابحاث'])

with tab1:
    st.write('اختار اسمك من القائمة:')
    name = st.selectbox('اسمك:', researchers)
    if st.button('ادخل غرفة النقاش'):
        st.session_state['selected'] = name
    if 'selected' in st.session_state:
        name = st.session_state['selected']
        st.markdown('### مرحبا ' + name)
        st.markdown('### غرفة النقاش - كل الباحثين سوا')
        new_msg = st.text_area('اكتب رسالتك هنا...', key='msg_general')
        if st.button('انشر رسالتي', key='send_general'):
            if new_msg.strip() != '':
                data['chats'].append({'name': name, 'text': new_msg})
                save_data(data); st.success('اتنشرت رسالتك'); st.rerun()
            else: st.warning('اكتب حاجة اولا')
        st.markdown('---')
        st.write('رسائل كل الباحثين:')
        if data['chats']:
            for m in reversed(data['chats']): st.info(m['name'] + ' : ' + m['text'])
        else: st.write('لسه ما في
