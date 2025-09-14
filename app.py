### Food Nutriants Applications
import os
import streamlit as st 
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

# set configure to access gemini models
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to get response 
def get_response(input_prompt, image):
    model=genai.GenerativeModel(model_name="gemini-2.5-flash")
    response=model.generate_content([input_prompt, image[0]])
    return response.text

## Preprocess the input image 
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        
        bytes_data= uploaded_file.getvalue() 
        image_parts= [
          {
            "mime_type": uploaded_file.type, 
            "data": bytes_data
          }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded, please uploade a image file")
    
## Set the streamlit web app
st.set_page_config(page_title="Nutriants Advisor App")
st.header("Nutriants Advisor Application: Calculate the Calories of Foods:")
uploaded_file= st.file_uploader("Choose an Image ...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    

## Set the input prompts 
input_prompt= """
You are an expert in nutritionist where you need to see the food items from the image 
       and calculate the total calories, also provide the details of 
       every food items with calories intake
       in below format
    
      1. Item 1 - no of calories
      2. Item 2 - no of calories
      ----
      ----
Finally you can mention whether the food is healthy or not and also mention
the percentage split of the ratio of carbohydrates, fats, fibers, sugar and other
important things in our diet 

"""

submit=st.button("Calculate the Total Calories of My Foods")
if submit:
    image_data= input_image_setup(uploaded_file)
    response= get_response(input_prompt, image_data)
    st.subheader("The Response is ")
    st.write(response)