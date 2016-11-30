import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from metric_funcs import mape

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

    def __init__(self, data, **kwargs):

        #Load dataset.
        self.df = pd.read_csv(data, index_col=0, parse_dates=True)

        #Init model with tuning parameters.
        self.model = RandomForestRegressor(*kwargs)

        #Init train, test, variables.
        self.y_train = None
        self.X_train = None
        self.y_test = None
        self.X_test = None

        self.test_index = None

    def cross_val(self, error = mean_squared_error, training_time = '3W', **kwargs):

        '''
        Cross validation timeseries.

        training_time: str, default = '3W'
            Time to train a single prediction task.
            (Eg. To cross validate this model we need:
                - generate partitions of training set given by the training time per task
                - each task will be trained-tested
                - compute average MSE for all tasks

        Returns
        ------

        MSE: List
            List with MSE errors from each Random Forest predictor.

        '''

        # Set last day to avoid out-of-bounds indices when training last k fold.
        last_task_day = self.df.index.date[-1]
        # Get list of indeces for in-sample validation.
        task_indeces = self.df.resample(training_time).indices.values()
        # One day timedelta.
        one_day = pd.Timedelta('1D')

        # List of error from CV.
        MSE = []

        for task in task_indeces:

            # Index main dataframe with task.
            df_task = self.df.iloc[task]

            #Train timeframes
            train_start = df_task.index[0]
            train_end = df_task.index[-1]

            #get last in task to use as proxy for the next day.
            task_proxy = df_task.index.date[-1]
            if last_task_day == task_proxy:
                # In case it is, re-index one day before.
                train_end = train_end-one_day

            #Test timeframes
            test_start = train_end + pd.Timedelta('15m')
            test_end = test_start + one_day

            #Vectorize training-test data.
            self.vectorize(train_start, train_end, test_start, test_end)

            #Fit-Predict
            self.model = RandomForestRegressor(**kwargs)
            self.model.fit(self.X_train, self.y_train)
            y_predict = self.model.predict(self.X_test)

            MSE.append(error(self.y_test, self.y_predict))

        return MSE

    def vectorize(self, train_start, train_end, test_start, test_end):

        '''
        Vectorize dataframe for algorithm consumption.

        indices: DateTimeIndex
            Indices to slice main dataframe.

        Returns
        ------
        y_train, X_train, y_test, y_test: numpy array

        '''
        df_train  = self.df[train_start:train_end]
        df_test = self.df[test_start:test_end]

        #Get index for plotting afterwards.
        self.test_index = df_test.index

        self.y_train = df_train.pop('kwh')
        self.X_train = df_train.values

        self.y_test = df_test.pop('kwh')
        self.X_test = df_test.values

if __name__ == '__main__':
    pass
