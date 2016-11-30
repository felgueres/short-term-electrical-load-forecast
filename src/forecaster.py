import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

class Forecaster(object):
    '''
    Forecasts 24-hr horizon load at 15-min intervals using a Random Forest Regressor.

    Parameters
    ----------
    path: str
        Path to csv file.

    kwargs: dict
        Parameters for sklearn RandomForestClassifier

    '''

    def __init__(self, data, splits_cross_val = 12, **kwargs):

        #Load dataset.
        self.df = pd.read_csv(data, index_col=0, parse_dates=True)

        #Initialize model with tuning parameters.
        self.model = RandomForestRegressor(**kwargs)

        #Set number of splits for cross validation
        self.splits_cross_val = splits_cross_val

        #set response variable
        self.y = self.df.pop('kwh')

        #set feature space
        self.X = self.df.values

    def cross_validation(self):

        '''
        Create train-validate for cross validation.

        training_time: str
            Time to train a single prediction task.
            (Eg. To cross validate this model we need:
                - generate as many partitions as possible given the number of splits
                - each task will be trained-tested
                - compute average MSE for all tasks

        Output
        ------

        '''
        pass

    def cross_val(self):

        tscv = TimeSeriesSplit(n_splits = self.splits_cross_val)

        for train, test in tscv.split(self.X):
            print("%s %s" % (train, test))

if __name__ == '__main__':
    pass
