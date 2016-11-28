import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split

class forecaster(object):
    '''
    Forecasts load.

    Parameters
    ----------

    path: str
        Path to csv file.

    model: str
        Model type:
        - ‘RF’ : Random Forest (default)

    '''

    def __init__(self, path, model = 'RF'):

        self.df = pd.read_csv(path, index_col=0, parse_dates=True)

        # Create features for specified model.

        if model == 'RF':

            self._featurize_randomforest()

    def _featurize_randomforest(self):
        '''
        Build features for random forest.
        '''
        pass

    def _features_d(self):
        '''
        Create features:
        - min values for day d
        - max values for day d
        '''
        pass

    def _features_d_minus_1(self):
        '''
        Create features:
        - load of day d-1 at time interval h
        - morning load peak of d-1
        - evening load peak of d-1
        '''
        pass

    def fit(self):
        '''
        Fit specified model.
        '''
        pass

    def predict(self):
        '''
        Predict in-sample and out-of-sample cases.
        '''
        pass

    def plot_in_sample(self):
        '''
        Plot actual vs. predicted.
        '''
        pass

    def plot_error(self):
        '''
        Plot error distribution.
        '''
        pass
        
if __name__ == '__main__':
    pass
