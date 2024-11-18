import os
import pandas as pd
import numpy as np
import sys
from src.Exception import CustomException
from src.logger import logging
from src.Utils import load_object

class Predict:
    def __init__(self):
        pass
    def predict(self,features):
        try:
            model_path = os.path.join('artifacts','model.pkl')
            preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

            logging.info("Loading Model & Preprocessing Objects")
            
            model = load_object(model_path)

            preprocessor = load_object(preprocessor_path)

            features['sex'] = features['sex'].map({'male':0,'female':1})
            features['smoker'] = features['smoker'].map({'no':0,'yes':1})

            scaled_data = preprocessor.transform(features)

            Predictions = model.predict(scaled_data)

            logging.info(f"Predictions on new data Completed,the predicted value is {Predictions}")

            return Predictions 
            
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:

    def __init__(self,age,sex,bmi,children,smoker,region):
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.region = region
        

    logging.info('Creating Data as DataFrame')

    def get_data_as_dataframe(self):
        try:
            CustomData_dictionary = {
                'age':[self.age],
                'sex':[self.sex],
                'bmi':[self.bmi],
                'children':[self.children],
                'smoker':[self.smoker],
                'region':[self.region]
            }
            return pd.DataFrame(CustomData_dictionary)
        except Exception as e:
            raise CustomException(e,sys)
        