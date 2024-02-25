import streamlit as st
from PIL import Image
from io import BytesIO  



@st.cache_resource
def model_inference(image) -> float:
    from PIL import Image
    from transformers import CLIPProcessor, CLIPModel


    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    Pilimage = Image.open(image)

    inputs = processor(text=["Histopathology image","X-ray image (Chest)","MRI Scan image (Brain)","others"], images=Pilimage, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities



    return probs.detach().numpy()[0][0] ,probs.detach().numpy()[0][1],probs.detach().numpy()[0][2], probs.detach().numpy()[0][3]


def Model_Inference():
    st.session_state.Image_object = BytesIO(st.session_state.Image.getvalue())
    return model_inference(st.session_state.Image_object)





if "user_logged" not in st.session_state:
    st.session_state.user_logged = False

if "Image_object" not in st.session_state:
    st.session_state.Image_object= None

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







Inference,Results,Navigation=st.tabs(["Inference","Results","Navigation"])


with Inference:
    st.write("Get Good Advice")
    st.file_uploader("Upload An X-ray scan of the chest or an MRI scan of the brain or a Histopathology image of breast tissue",key="Image")

    




with Results:

    if st.session_state.Image != None:
        st.image(st.session_state.Image.getvalue())


        Histopathology_image,X_ray_image,Mri_scan,others=Model_Inference()

        if Histopathology_image >X_ray_image and Histopathology_image> Mri_scan:

            st.markdown("Histopathology ")# code for using histopathology model

        elif X_ray_image>Histopathology_image and X_ray_image> Mri_scan:

            st.markdown("Xray ")# code for using Xray model

        elif Mri_scan>Histopathology_image and Mri_scan>X_ray_image:

            st.markdown("Brain cancer ")# code for using Breast cancer model

        else:
            st.markdown(others)







with Navigation:
    if st.button("Chat with your medical result and history"):
        st.switch_page('pages/chat.py')
    if st.button("Previous results"):
        st.switch_page('pages/history.py')





