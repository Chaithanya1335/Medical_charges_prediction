from src.Pipeline.Predict_Pipeline import CustomData
from src.Pipeline.Predict_Pipeline import Predict
from src.Exception import CustomException
import sys 
from src.logger import logging
import streamlit as st

st.set_page_config('Medical Charges Prediction')

st.title(':blue[Medical Charges prediction for Insurance Claim]')
with st.container(border=True,):
    age = st.number_input('Age',min_value=1,step=1,value=20,label_visibility="visible")

    sex = st.radio("sex",options=['male','female'],horizontal=True)

    bmi = st.number_input(label="BMI",min_value=1,step=1)

    children = st.radio("Children",options=[1,2,3,4,5],horizontal=True)

    smoker = st.radio("Smoker",options=['yes','no'],horizontal=True)

    region = st.selectbox("Region",options=['southwest','southeast','northwest','northeast'])


class App:
    def __init__(self):
        pass

    logging.info(" Getting data as DataFrame ")

    def getting_data_as_DataFrame(age,sex,bmi,children,smoker,region):
        try:

            data = CustomData(age,sex,bmi,children,smoker,region).get_data_as_dataframe()

            logging.info(" data is Converted to DataFrame ")

            return data
        except Exception as e:
            raise CustomException(e,sys)
        
    def display_results(data):
        try:
            predictions = Predict().predict(data)

            container = st.container(border=True)

            container.write(f":blue[The Predicted Medical charges are{predictions}]")

            logging.info("Prediction Displayed on Streamlit console")
        except Exception as e:
            raise CustomException(e,sys)
        
if st.button(":green[Predict]",use_container_width=True):
    data = App.getting_data_as_DataFrame(age=age,sex=sex,bmi=bmi,children=children,smoker=smoker,region=region)

    display_results = App.display_results(data)








