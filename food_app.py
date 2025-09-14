### Food Nutriants Applications
import streamlit as st
from PIL import Image
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]= os.getenv("GOOGLE_API_KEY")
api_key= st.secrets["GOOGLE_API_KEY"]

# set configure to access gemini models
from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

## Function to get response 
def get_response(input_prompt, image):
    response=llm.invoke([input_prompt, image[0]])
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
st.secrets["GOOGLE_API_KEY"]
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