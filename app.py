import streamlit as st
import os, json

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

tab1, tab2, tab3 = st.tabs(['اضف بحثك', 'الباحثون', 'الابحاث'])

with tab1:
    st.subheader('اضف بحثك')
    title = st.text_input('عنوان البحث')
    author = st.selectbox('اسمك', researchers)
    uploaded = st.file_uploader('ارفع ملف البحث (PDF)', type=['pdf'])
    if st.button('انشر البحث'):
        if title and uploaded:
            os.makedirs('uploads', exist_ok=True)
            path = os.path.join('uploads', uploaded.name)
            with open(path,'wb') as f: f.write(uploaded.getbuffer())
            data['papers'].append({'title':title,'author':author,'file':path})
            save_data(data); st.success('اتنشر بحثك ✅')
        else: st.warning('اكتب العنوان وارفع الملف')

with tab2:
    st.subheader('الباحثون')
    st.write('اضغط على اسمك عشان تخش غرفة النقاش الواحدة')
    for name in researchers:
        if st.button(name, key='btn_'+name):
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
        else: st.write('لسه ما في رسائل')

with tab3:
    st.subheader('الابحاث')
    if not data['papers']: st.write('لسه ما في ابحاث منشورة')
    for p in reversed(data['papers']):
        st.markdown(f"**{p['title']}** - بواسطة {p['author']}")
        if os.path.exists(p['file']):
            with open(p['file'],'rb') as f:
                st.download_button(f"تحميل {p['title']}", f, file_name=os.path.basename(p['file']), key=p['title']+p['author'])
        st.markdown('---')
