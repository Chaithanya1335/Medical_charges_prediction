import pickle
import sys
import os
from src.Exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
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
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
def evaluate_models(x_train,x_test,y_train,y_test,models,params):
    try:
        report={}
        for i in range(len(models)):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model,param,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)

            model.fit(x_train,y_train)

            y_pred = model.predict(x_test)

            model_score = r2_score(y_test,y_pred=y_pred) 

            report[list(models.keys())[i]] = model_score

            return report
        
    except Exception as e:
        raise CustomException(e,sys)


