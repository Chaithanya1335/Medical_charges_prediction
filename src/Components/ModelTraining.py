import os
import sys
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.Exception import CustomException
from src.logger import logging
from src.Utils import save_object,evaluate_models
from dataclasses import dataclass

@dataclass
class ModelTrainingConfig:
    model_obj_path = os.path.join("artifacts",'model.pkl')

class ModelTraining:
    def __init__(self) -> None:
        self.ModelTrainingConfig = ModelTrainingConfig()
    def initiate_model_Training(self,train_arr,test_arr):
        logging.info("Splitting Training and Testing Input Data")
        try:
            x_train,y_train,x_test,y_test = (train_arr[:,:-1],
                                            train_arr[:,-1],
                                            test_arr[:,:-1],
                                            test_arr[:,-1])
            models = {
                    "Random Forest": RandomForestRegressor(),
                    "Decision Tree": DecisionTreeRegressor(),
                    "Gradient Boosting": GradientBoostingRegressor(),
                    "Linear Regression": LinearRegression(),
                    "XGBRegressor": XGBRegressor(),
                    "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                    "AdaBoost Regressor": AdaBoostRegressor(),
                }
            
            params={
                    "Decision Tree": {
                        'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                        # 'splitter':['best','random'],
                        # 'max_features':['sqrt','log2'],
                    },
                    "Random Forest":{
                        # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    
                        # 'max_features':['sqrt','log2',None],
                        'n_estimators': [8,16,32,64,128,256]
                    },
                    "Gradient Boosting":{
                        # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                        'learning_rate':[.1,.01,.05,.001],
                        'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                        # 'criterion':['squared_error', 'friedman_mse'],
                        # 'max_features':['auto','sqrt','log2'],
                        'n_estimators': [8,16,32,64,128,256]
                    },
                    "Linear Regression":{},
                    "XGBRegressor":{
                        'learning_rate':[.1,.01,.05,.001],
                        'n_estimators': [8,16,32,64,128,256]
                    },
                    "CatBoosting Regressor":{
                        'depth': [6,8,10],
                        'learning_rate': [0.01, 0.05, 0.1],
                        'iterations': [30, 50, 100]
                    },
                    "AdaBoost Regressor":{
                        'learning_rate':[.1,.01,0.5,.001],
                        # 'loss':['linear','square','exponential'],
                        'n_estimators': [8,16,32,64,128,256]
                    }
                    
                }
            
            model_report:dict=evaluate_models(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test,models=models,params=params)
            
            best_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_score)]

            best_model = models[best_model_name]

            if best_score<0.6:
                logging.info("No best Model Found !")
            logging.info("Best model Found on Training and Testing Data")

            save_object(
                file_path=self.ModelTrainingConfig.model_obj_path,
                preprocessor_obj=best_model
            )

            r2_score = model_report[best_model_name]

            logging.info(f"r2score achieved with {best_model_name} Model is : {r2_score}")

            return r2_score
        except Exception as e:
            raise CustomException(e,sys)

                                             