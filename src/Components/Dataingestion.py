import sys
import os
import pandas as pd
from src.Exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngetionConfig:
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','raw.csv')
class DataIngestion:
    def __init__(self) -> None:
        self.DataIngestionConfig = DataIngetionConfig()
    def intiate_dataingestion(self):
        logging.info('Entered Data Ingestion Component')
        try:
            data = pd.read_csv('insurance.csv')
            logging.info('Data is read as the DataFrame')
            os.makedirs(os.path.dirname(self.DataIngestionConfig.train_data_path),exist_ok=True)
            data.to_csv(self.DataIngestionConfig.raw_data_path,index=False,header=True)
            logging.info('Train Test Split Intiated')
            train_data,test_data = train_test_split(data,test_size=0.2,random_state=42)
            train_data.to_csv(self.DataIngestionConfig.train_data_path,index=False,header=True)
            test_data.to_csv(self.DataIngestionConfig.test_data_path,index=False,header=True)
            logging.info('Data Ingestion Completed')
            return (self.DataIngestionConfig.train_data_path,self.DataIngestionConfig.test_data_path)
        except Exception as e:
            raise CustomException(e,sys)
if __name__ =='__main__':
    train_data_path,test_data_path = DataIngestion().intiate_dataingestion()