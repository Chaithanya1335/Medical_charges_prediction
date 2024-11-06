import os
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.Exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.Utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path  = os.path.join("artifacts",'preprocessor.pkl')

class DataTransformation:
    def __init__(self) :
        self.DataTransformationConfig = DataTransformationConfig()
    def get_preprocessing_object(self,num_cols,cat_cols):
        '''This function is responsible for data Transformation'''
        try:
            num_pipeline = Pipeline([
                ('scaler',StandardScaler())
            ])
            cat_pipeline = Pipeline([
                ('encoder',OneHotEncoder(handle_unknown='ignore')),
                ('scaler',StandardScaler(with_mean=False))
            ])

            logging.info(f"Numerical Columns : {num_cols}")
            logging.info(f"Categorical Columns : {cat_cols}")

            preprocessor = ColumnTransformer([
                ('num_pipeline',num_pipeline,num_cols),
                ('cat_pipeline',cat_pipeline,cat_cols)
            ])
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_Transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            train_df['sex'] = train_df['sex'].map({'male':0,'female':1})
            train_df['smoker'] = train_df['smoker'].map({'yes':1,'no':0})


            test_df['sex'] = test_df['sex'].map({'male':0,'female':1})
            test_df['smoker'] = test_df['smoker'].map({'yes':1,'no':0})

            input_features_train_df = train_df.drop(columns=['charges'],axis=1)
            target_feature_train_df = train_df['charges']

            input_features_test_df = test_df.drop(columns=['charges'],axis = 1)
            target_feature_test_df = test_df['charges']

            num_cols = input_features_train_df.select_dtypes(exclude='O').columns.to_list()
            cat_cols = input_features_train_df.select_dtypes(include = 'O').columns.to_list()

            logging.info('Train Test Data Reading Completed')

            logging.info('Getting Preprocessor Object')

            preprocessor = self.get_preprocessing_object(num_cols=num_cols,cat_cols=cat_cols)

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_features_train_arr = preprocessor.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessor.transform(input_features_test_df)

            train_arr = np.c_[input_features_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_features_test_arr,np.array(target_feature_test_df)]

            logging.info('preprocessing Object saved')

            save_object(
                file_path=  self.DataTransformationConfig.preprocessor_obj_file_path,
                preprocessor_obj = preprocessor
            )
            logging.info('Data Transformation completed')
            return (train_arr,test_arr,self.DataTransformationConfig.preprocessor_obj_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)
        



