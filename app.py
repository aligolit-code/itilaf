import streamlit as st
import os, json
import arabic_reshaper
from bidi.algorithm import get_display

def ar(t):
    return get_display(arabic_reshaper.reshape(str(t)))

st.set_page_config(page_title='باحثين الائتلاف السوداني', layout='centered')

st.markdown("""
<style>
.main-title{ font-size:36px; font-weight:900; text-align:center; color:#111; }
.sub-title{ text-align:center; color:#555; font-size:16px; }
.stButton>button{ background:#FFD700 !important; color:#000 !important; font-size:20px; font-weight:bold; border-radius:20px; border:2px solid #FFC400; width:100%; padding:15px; }
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

st.markdown('<div class="main-title">باحثين الائتلاف السوداني</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">الاوراق العلمية، والفرص البحثية في مكان واحد</div>', unsafe_allow_html=True)
st.markdown('---')

researchers = ['مستر ناجي','دكتورة نادية','نشوى','مكارم','ثويبة','فكتوريا','علي','هديل','هناء','سعاد','صالح','رحاب','سليمى','معاذ','أمنة']

tab1, tab2, tab3 = st.tabs([ar('اضف بحثك'), ar('الباحثون'), ar('الابحاث')])

with tab1:
    st.subheader(ar('اضف بحثك'))
    title = st.text_input(ar('عنوان البحث'))
    author = st.selectbox(ar('اسمك'), [ar(x) for x in researchers])
    uploaded = st.file_uploader(ar('ارفع ملف البحث (PDF)'), type=['pdf'])
    if st.button(ar('انشر البحث')):
        if title and uploaded:
            os.makedirs('uploads', exist_ok=True)
            path = os.path.join('uploads', uploaded.name)
            with open(path,'wb') as f: f.write(uploaded.getbuffer())
            data['papers'].append({'title':title,'author':author,'file':path})
            save_data(data); st.success(ar('اتنشر بحثك'))
        else: st.warning(ar('اكتب العنوان وارفع الملف'))

with tab2:
    st.subheader(ar('الباحثون'))
    st.write(ar('اضغط على اسمك عشان تخش غرفة النقاش الواحدة'))
    for name in researchers:
        if st.button(ar(name), key='btn_'+name):
            st.session_state['selected'] = name
    if 'selected' in st.session_state:
        name = st.session_state['selected']
        st.markdown('### مرحبا ' + name)
        st.markdown('### غرفة النقاش - كل الباحثين سوا')
        new_msg = st.text_area(ar('اكتب رسالتك هنا...'), key='msg_general')
        if st.button(ar('انشر رسالتي'), key='send_general'):
            if new_msg.strip() != '':
                data['chats'].append({'name': name, 'text': new_msg})
                save_data(data); st.success(ar('اتنشرت رسالتك')); st.rerun()
            else: st.warning(ar('اكتب حاجة اولا'))
        st.markdown('---')
        st.write(ar('رسائل كل الباحثين:'))
        if data['chats']:
            for m in reversed(data['chats']): st.info(m['name'] + ' : ' + m['text'])
        else: st.write(ar('لسه ما في رسائل'))

with tab3:
    st.subheader(ar('الابحاث'))
    if not data['papers']: st.write(ar('لسه ما في ابحاث منشورة'))
    for p in reversed(data['papers']):
        st.markdown(f"**{p['title']}** - بواسطة {p['author']}")
        if os.path.exists(p['file']):
            with open(p['file'],'rb') as f:
                st.download_button(ar('تحميل ') + p['title'], f, file_name=os.path.basename(p['file']), key=p['title']+p['author'])
        st.markdown('---')
