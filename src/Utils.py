import pickle
import sys
import os
from src.Exception import CustomException

def save_object(file_path,preprocessor_obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(preprocessor_obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)

