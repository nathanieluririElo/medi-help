import streamlit as st

from database import db_login_signup

if "UD" not in st.session_state:
    st.session_state.UD = None
if "type" not in st.session_state:
    st.session_state.type = "R"


RformLayout = st.empty()
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__qRIco{display:None;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



def unique(username:str)->bool:
    # print("Db unique check= ",db_login_signup(3,username,"none"))
    if db_login_signup(3,username,"none") == False:
        st.warning(f"User name already exists")
    return db_login_signup(3,username,"none")

def Password_Check():
    if st.session_state.rpassword.strip()=='':
        return False
    else:

        if st.session_state.rpassword == st.session_state.cpassword:
            return  True
        else:
            st.warning(f"Check Your Password {st.session_state.rpassword} is not equals {st.session_state.cpassword}")
            return False


def registerPage():    
    with RformLayout.container():
        st.title("Register Page")
        st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)
        st.text_input("Enter A Username",max_chars=20,key='rusername_field',help='Maximum of 20 characters')
        st.text_input("Enter A Password",max_chars=20,key='rpassword',type='password',help='Maximum of 20 characters')
        st.text_input("Confirm Your Password",max_chars=20,key='cpassword',type='password',help='Maximum of 20 characters')
        if unique(st.session_state.rusername_field)==True and Password_Check()==True : 
            with st.form(key="anxiety",border=True):
            
                st.text_input("Enter Your First Name",max_chars=20,key="fname_field",help="Maximum of 20 characters")
                st.text_input("Enter Your Last Name",max_chars=20,key= 'lname_field')
                st.number_input("How quickly can you learn new things on a scale of 1-10",min_value=1, max_value=10, key='speed_learn_field')
                st.number_input("How quickly can you understand things on a scale of 1-10",min_value=1,max_value=10,key="understanding_rate_field")
                st.form_submit_button(label="Submit")
                if st.session_state.fname_field.strip() and st.session_state.lname_field.strip() and st.session_state.rpassword.strip() and st.session_state.rusername_field.strip():
                    st.session_state.UD =db_login_signup(1, st.session_state.rusername_field, st.session_state.rpassword,first_name=st.session_state.fname_field,last_name=st.session_state.lname_field,learning_rate=st.session_state.speed_learn_field,understanding_rate=st.session_state.understanding_rate_field)
                    st.session_state.user_logged=True
               
    if st.button("Click here to Login", key="register_button"):
        # db_login_signup(1, "testy", "p",first_name="Test",last_name="Test",learning_rate="2",understanding_rate="4")
        st.session_state.type = "L"
        st.rerun() 


if __name__ =="__main__":
    registerPage()


if st.session_state.type == "L":
    st.switch_page('pages/login.py')


if st.session_state.UD !=None:
    
    st.switch_page('app.py')
    
