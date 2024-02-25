import streamlit as st


if "user_logged" not in st.session_state:
    st.session_state.user_logged = False

if st.session_state.user_logged == False:
    st.switch_page('pages/register.py')


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__qRIco{display:None;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)







History,Results,Navigation=st.tabs(["History","Results","Navigation"])

with History:
    st.write("Get Good Advice")
    st.file_uploader("Upload An X-ray",type='png',key="Image")



with Results:

    st.write(f"Results {st.session_state.Image.name}")
    
    st.image(st.session_state.Image.getvalue())





with Navigation:

    if st.button("Home"):
        pass

    if st.button("Chat with your medical result and history"):
        pass




