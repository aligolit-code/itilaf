import streamlit as st
import os, json

st.set_page_config(page_title='منصة باحثي الائتلاف السوداني', layout='centered')
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@900&display=swap" rel="stylesheet">', unsafe_allow_html=True)

css = '.main-title{font-family:Amiri,Cairo,serif;font-size:38px;font-weight:700;text-align:center;background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700,#00B894);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}'
css += '.sub-title{font-family:Cairo,sans-serif;text-align:center;color:#666;font-size:16px;}'
css += '.stButton>button{background:linear-gradient(45deg,#FFD700,#FFEA00);color:#000;font-size:20px;font-weight:bold;border-radius:20px;border:2px solid #FFC400;box-shadow:0 0 20px #FFD700;width:100%;padding:15px;}'
st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)

# --- حفظ دائم في ملف ---
def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json','r',encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {"chats": {}, "papers": []}

def save_data(data):
    with open('data.json','w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if 'data' not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

for f in os.listdir('.'):
    if f.startswith('Screenshot') and (f.endswith('.jpg') or f.endswith('.png')):
        st.image(f, use_container_width=True)
        break

st.markdown('<div class="main-title">منصة باحثي الائتلاف السوداني</div>', unsafe_allow_html=True)
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
            save_data(data)
            st.success('اتنشر بحثك ✅')
        else:
            st.warning('اكتب العنوان وارفع الملف')

with tab2:
    st.subheader('الباحثون')
    st.write('اضغط على اسمك واكتب طوالي')
    for name in researchers:
        if st.button(name, key='btn_'+name):
            st.session_state['selected'] = name
    if 'selected' in st.session_state:
        name = st.session_state['selected']
        st.markdown('### مرحبا ' + name)
        st.markdown('### مكان النقاش الخاص بـ ' + name)
        new_msg = st.text_area('اكتب رسالتك هنا...', key='msg_'+name)
        if st.button('انشر رسالتي', key='send_'+name):
            if new_msg.strip() != '':
                if name not in data['chats']: data['chats'][name] = []
                data['chats'][name].append(new_msg)
                save_data(data)
                st.success('اتنشرت رسالتك')
                st.rerun()
            else:
                st.warning('اكتب حاجة اولا')
        st.markdown('---')
        st.write('رسائلك المنشورة:')
        msgs = data['chats'].get(name, [])
        if msgs:
            for m in reversed(msgs): st.info(m)
        else: st.write('لسه ما كتبت حاجة')

with tab3:
    st.subheader('الابحاث')
    if not data['papers']:
        st.write('لسه ما في ابحاث منشورة')
    for p in reversed(data['papers']):
        st.markdown(f"**{p['title']}** - بواسطة {p['author']}")
        if os.path.exists(p['file']):
            with open(p['file'],'rb') as f:
                st.download_button(f"تحميل {p['title']}", f, file_name=os.path.basename(p['file']), key=p['title']+p['author'])
        st.markdown('---')
