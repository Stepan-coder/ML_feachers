import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict, List
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from Ra_feature_package.Errors import Errors
from Ra_feature_package.models.static_methods import *


class RFRegressor:
    def __init__(self,
                 task: pd.DataFrame,
                 target: pd.DataFrame,
                 train_split: int,
                 show: bool = False):
        """
        This method is the initiator of the RFRegressor class
        :param task: The training part of the dataset
        :param target: The target part of the dataset
        :param train_split: The coefficient of splitting into training and training samples
        :param show: The parameter responsible for displaying the progress of work
        """
        self.text_name = "RandomForestRegressor"
        self.default_param_types = {'n_estimators': int,
                                    'criterion': str,
                                    'max_depth': int,
                                    'min_samples_split': int or float,
                                    'min_samples_leaf': int,
                                    'min_weight_fraction_leaf': float,
                                    'max_features': str,
                                    'max_leaf_nodes': int,
                                    'min_impurity_decrease': float,
                                    'min_impurity_split': float,
                                    'bootstrap': bool,
                                    'oob_score': bool,
                                    'n_jobs': int,
                                    'verbose': int,
                                    'warm_start': bool,
                                    'ccp_alpha': float,
                                    'max_samples': int or float}

        self.default_param = {'n_estimators': 100,
                              'criterion': "mse",
                              'max_depth': None,
                              'min_samples_split': 2,
                              'min_samples_leaf': 1,
                              'min_weight_fraction_leaf': 0.0,
                              'max_features': "auto",
                              'max_leaf_nodes': None,
                              'min_impurity_decrease': 0.0,
                              'min_impurity_split': None,
                              'bootstrap': True,
                              'oob_score': False,
                              'n_jobs': None,
                              'verbose': 0,
                              'warm_start': False,
                              'ccp_alpha': 0.0,
                              'max_samples': None}

        count = len(task.keys()) + 1
        self.default_params = {'n_estimators': conf_params(min_val=2, max_val=count, count=count, ltype=int),
                               'criterion': ["mse", "mae"],
                               'max_depth': conf_params(min_val=2, max_val=count * 2, count=count, ltype=int),
                               'min_samples_split': conf_params(min_val=2, count=count, ltype=int),
                               'min_samples_leaf': conf_params(min_val=2, count=count, ltype=int),
                               'min_weight_fraction_leaf': [0.],
                               'max_features': ['sqrt', 'auto', 'log2', None],
                               'max_leaf_nodes': [None],
                               'min_impurity_decrease': [0.0],
                               'min_impurity_split': [None],
                               'bootstrap': [True],
                               'oob_score': [True, False],
                               'n_jobs': [None],
                               'verbose': [0],
                               'warm_start': [True, False],
                               'ccp_alpha': [0.0],
                               'max_samples': conf_params(min_val=2, max_val=count, count=count, ltype=int)}
        self.locked_params = ['criterion', 'max_features', 'bootstrap', 'oob_score', 'warm_start']
        self.importance = {}
        self.is_model_fit = False
        self.is_grid_fit = False

        self.show = show
        self.model = None
        self.grid_best_params = None
        self.keys = task.keys()
        self.keys_len = len(task.keys())
        self.X_train, self.x_test, self.Y_train, self.y_test = train_test_split(task,
                                                                                target,
                                                                                train_size=train_split,
                                                                                random_state=13)

    def __str__(self):
        return f"'<Ra.{RFRegressor.__name__} model>'"

    def __repr__(self):
        return f"'<Ra.{RFRegressor.__name__} model>'"

    def predict(self, data: pd.DataFrame):
        return self.model.predict(data)

    def fit(self,
            param_dict: Dict[str, int or str] = None,
            grid_params: bool = False):
        f"""
        This method trains the model {self.text_name}, it is possible to use the parameters from "fit_grid"
        :param param_dict: The parameter of the hyperparameter grid that we check
        :param grid_params: The switcher which is responsible for the ability to use all the ready-made parameters
         from avia for training
        """
        if grid_params and param_dict is None:
            self.model = RandomForestRegressor(n_estimators=self.grid_best_params['n_estimators'],
                                               criterion=self.grid_best_params['criterion'],
                                               max_depth=self.grid_best_params['max_depth'],
                                               min_samples_split=self.grid_best_params['min_samples_split'],
                                               min_samples_leaf=self.grid_best_params['min_samples_leaf'],
                                               min_weight_fraction_leaf=self.grid_best_params['min_weight_fraction_leaf'],
                                               max_features=self.grid_best_params['max_features'],
                                               max_leaf_nodes=self.grid_best_params['max_leaf_nodes'],
                                               min_impurity_decrease=self.grid_best_params['min_impurity_decrease'],
                                               min_impurity_split=self.grid_best_params['min_impurity_split'],
                                               bootstrap=self.grid_best_params['bootstrap'],
                                               oob_score=self.grid_best_params['oob_score'],
                                               n_jobs=self.grid_best_params['n_jobs'],
                                               verbose=self.grid_best_params['verbose'],
                                               warm_start=self.grid_best_params['warm_start'],
                                               ccp_alpha=self.grid_best_params['ccp_alpha'],
                                               max_samples=self.grid_best_params['max_samples'],
                                               random_state=13)
        elif not grid_params and param_dict is not None:
            model_params = self.default_param
            for param in param_dict:
                if param not in self.default_params.keys():
                    raise Exception(f"The column {param} does not exist in the set of allowed parameters!")
                check_param(param,
                            param_dict[param],
                            self.default_param_types[param],
                            type(self.default_param[param]))
                model_params[param] = param_dict[param]

            self.model = RandomForestRegressor(n_estimators=model_params['n_estimators'],
                                               criterion=model_params['criterion'],
                                               max_depth=model_params['max_depth'],
                                               min_samples_split=model_params['min_samples_split'],
                                               min_samples_leaf=model_params['min_samples_leaf'],
                                               min_weight_fraction_leaf=model_params['min_weight_fraction_leaf'],
                                               max_features=model_params['max_features'],
                                               max_leaf_nodes=model_params['max_leaf_nodes'],
                                               min_impurity_decrease=model_params['min_impurity_decrease'],
                                               min_impurity_split=model_params['min_impurity_split'],
                                               bootstrap=model_params['bootstrap'],
                                               oob_score=model_params['oob_score'],
                                               n_jobs=model_params['n_jobs'],
                                               verbose=model_params['verbose'],
                                               warm_start=model_params['warm_start'],
                                               ccp_alpha=model_params['ccp_alpha'],
                                               max_samples=model_params['max_samples'],
                                               random_state=13)
        elif not grid_params and param_dict is None:
            self.model = RandomForestRegressor()
        else:
            raise Exception("You should only choose one way to select hyperparameters!")
        print(f"Learning {self.text_name}...")
        self.model.fit(self.X_train, self.Y_train.values.ravel())
        self.is_model_fit = True

    def fit_grid(self,
                 params_dict: Dict[str, list] = None,
                 count: int = 1,
                 cross_validation: int = 3):
        """
        This method uses iteration to find the best hyperparameters for the model and trains the model using them
        :param params_dict: The parameter of the hyperparameter grid that we check
        :param count: The step with which to return the values
        :param cross_validation: The number of sections into which the dataset will be divided for training
        """
        model_params = self.default_params
        if params_dict is not None:
            for param in params_dict:
                if param not in self.default_params.keys():
                    raise Exception(f"The column {param} does not exist in the set of allowed parameters!")
                check_param(grid_param=param,
                            value=params_dict[param],
                            param_type=self.default_param_types[param],
                            setting_param_type=type(self.default_params[param]))
                model_params[param] = params_dict[param]

        for param in [p for p in model_params if p not in self.locked_params]:
            model_params[param] = get_choosed_params(model_params[param], count=count)
        if self.show:
            print(f"Learning GridSearch {self.text_name}...")
            show_grid_params(model_params)
        model = RandomForestRegressor(random_state=13)
        grid = GridSearchCV(model, model_params, cv=cross_validation)
        grid.fit(self.X_train, self.Y_train.values.ravel())
        self.grid_best_params = grid.best_params_
        self.is_grid_fit = True

    def get_locked_params(self) -> List[str]:
        return self.locked_params

    def get_non_locked_params(self) -> List[str]:
        return [p for p in self.default_params if p not in self.locked_params]

    def get_default_param_types(self) -> dict:
        """
        :return: This method return default model param types
        """
        return self.default_param_types

    def get_default_param_values(self) -> dict:
        """
        :return: This method return default model param values
        """
        return self.default_param

    def get_default_grid_param_values(self) -> dict:
        """
        :return: This method return default model param values for grid search
        """
        return self.default_params

    def get_is_model_fit(self) -> bool:
        f"""
        This method return flag is_model_fit
        :return: is_model_fit
        """
        return self.is_model_fit

    def get_is_grid_fit(self) -> bool:
        f"""
        This method return flag get_is_grid_fit
        :return: get_is_grid_fit
        """
        return self.is_grid_fit

    def get_grid_best_params(self) -> dict:
        """
        This method return the dict of best params for this model
        :return: dict of best params for this model
        """
        if self.is_grid_fit:
            return self.grid_best_params
        else:
            raise Exception('At first you need to learn grid')

    def get_feature_importance(self) -> dict:
        """
        This method return dict of feature importance where key is the column of input dataset, and value is importance
        of this column
        :return: dict of column importance
        """
        if not self.is_model_fit:
            raise Exception(f"You haven't trained the {self.text_name} yet!")
        for index in range(len(self.model.feature_importances_)):
            self.importance[self.keys[index]] = self.model.feature_importances_[index]
        return {k: v for k, v in sorted(self.importance.items(), key=lambda item: item[1], reverse=True)}

    def get_roc_auc_score(self) -> float:
        f"""
        This method calculates the "roc_auc_score" for the {self.text_name} on the test data
        :return: roc_auc_score
        """
        if not self.is_model_fit:
            raise Exception(f"You haven't trained the {self.text_name} yet!")
        return Errors.get_roc_auc_score(self.y_test, self.model.predict(self.x_test))

    def get_mean_squared_error(self) -> float:
        """
        This method calculates the "mean_squared_error" for the {self.text_name} on the test data
        :return: mean_squared_error
        """
        if not self.is_model_fit:
            raise Exception(f"You haven't trained the {self.text_name} yet!")
        return Errors.get_mean_squared_error(self.y_test, self.model.predict(self.x_test))

    def get_mean_absolute_error(self) -> float:
        """
        This method calculates the "mean_absolute_error" for the {self.text_name} on the test data
        :return: mean_absolute_error
        """
        if not self.is_model_fit:
            raise Exception(f"You haven't trained the {self.text_name} yet!")
        return Errors.get_mean_absolute_error(self.y_test, self.model.predict(self.x_test))

    def get_predict_text_plt(self,
                             save_path: str = None,
                             show: bool = False):
        """
        This method automates the display/saving of a graph of prediction results with a real graph
        :param save_path: The path to save the graph on
        :param show: The parameter responsible for displaying the plot of prediction
        """
        if not self.is_model_fit:
            raise Exception(f"You haven't trained the {self.text_name} yet!")
        values = [i for i in range(len(self.x_test))]
        plt.title(f'Predict {self.text_name} at test data')
        plt.plot(values, self.y_test, 'g-', label='test')
        plt.plot(values, self.model.predict(self.x_test), 'r-', label='predict')
        plt.legend(loc='best')
        if save_path is not None:
            if not os.path.exists(save_path):  # Надо что то с путём что то адекватное придумать
                raise Exception("The specified path was not found!")
            plt.savefig(f"{save_path}\\Test predict {self.text_name}.png")
        if show:
            plt.show()
        plt.close()