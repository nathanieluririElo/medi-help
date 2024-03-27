import streamlit as st
from PIL import Image
from io import BytesIO  



@st.cache_resource
def prediction_on_brain_tumor(image):
    from keras.models import load_model  # TensorFlow is required for Keras to work
    from PIL import Image, ImageOps  # Install pillow instead of PIL
    import numpy as np


    model = load_model("brain tumor/keras_model.h5", compile=False)

    # Load the labels
    class_names = open("brain tumor/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    # Replace this with the path to your image
    image = Image.open(image)


    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1


    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    return class_name[2:],confidence_score

    





# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             .viewerBadge_link__qRIco{display:None;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)









with st.sidebar:
    
    st.file_uploader("Upload An  MRI scan of the brain",key="Image")

    




if st.session_state.Image != None:
    st.image(st.session_state.Image.getvalue())
    st.session_state.Image_object = BytesIO(st.session_state.Image.getvalue())
    
    st.markdown(f"Predicted class: {prediction_on_brain_tumor(st.session_state.Image_object)[0]}\nConfidence Score: {prediction_on_brain_tumor(st.session_state.Image_object)[1]}")











