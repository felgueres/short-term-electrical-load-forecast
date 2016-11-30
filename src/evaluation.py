import numpy as np
from metric_funcs import mape

class Evaluation(object):
    '''
    Produce model performance metric.

    Parameters
    ----------

    Return
    ------
    '''

    def __init__(self, forecaster):

        '''
        Init forecaster
        '''

        self.model = forecaster

    def get_scores(X_train, X_test, y_train, y_test, score):
        '''
        Returns in-sample and out-of-sample validation

        Parameters
        ----------

        score: function
            Function to output model performance.

        X_train, X_test, y_train, y_test: numpy arrays
            Values to train-predict.

        '''

        #Train test set.
        self.model.fit(X_train, y_train)

        #Predict response.
        y_pred = self.model.predict(X_test)

        #Return score
        return score(y_test, y_pred)


if __name__ == '__main__':
    pass
