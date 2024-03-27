import streamlit as st
from PIL import Image
from io import BytesIO  
from model import disease


@st.cache_resource
def model_inference(image) -> float:
    """
    This function is used to perform A zero shot classification  inference on the input image.  
    It takes an image file as input and returns a the probabilities of it being a Histopathology Image
    X-ray Image(chest) Mri Scan (Brain) Or others.
    """
    from PIL import Image
    from transformers import CLIPProcessor, CLIPModel


    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    Pilimage = Image.open(image)


    inputs = processor(text=["Histopathology image","X-ray image (Chest)","MRI Scan image (Brain)","others"], images=Pilimage, return_tensors="pt", padding=True)
  
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    # print(probs.detach().numpy()[0][0] ,probs.detach().numpy()[0][1],probs.detach().numpy()[0][2], probs.detach().numpy()[0][3])



    return probs.detach().numpy()[0][0] ,probs.detach().numpy()[0][1],probs.detach().numpy()[0][2], probs.detach().numpy()[0][3]





def Model_Inference():
    """
    Firstly the function get's the value of the image and turns it into a file like object
    using BytesIO() class. Then it takes that object and passes it as a parameter for the model_inference function.
    So that it can be read by the model.

    """
    st.session_state.Image_object = BytesIO(st.session_state.Image.getvalue())
    # st.code(st.session_state.Image.getvalue())
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

            st.markdown(f"This is an image of breast tissue: {Histopathology_image}")
            st.write(disease(pred='breast',image=st.session_state.Image_object))# code for using histopathology model

        elif X_ray_image>Histopathology_image and X_ray_image> Mri_scan and X_ray_image> others:

            st.markdown(f"This is an Xray of the chest: {X_ray_image} ")
            st.write(disease(pred='xray',image=st.session_state.Image_object))# code for using Xray model

        elif Mri_scan>Histopathology_image and Mri_scan>X_ray_image and Mri_scan>others :

            st.markdown(f"This is an MRI of the Brain {Mri_scan} ")# code for using Breast cancer model
            st.write(disease(pred='brainTumor',image=st.session_state.Image_object))


        elif others>X_ray_image and others >Mri_scan and others> Histopathology_image:
            st.markdown(f" others: {others}")







with Navigation:
    if st.button("Chat with your medical result and history"):
        st.switch_page('pages/chat.py')
    if st.button("Previous results"):
        st.switch_page('pages/history.py')





