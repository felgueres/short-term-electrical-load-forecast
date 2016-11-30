import numpy as np
from metric_funcs import mape

class Evaluation(object):
    '''
    Produce evaluation metric.

    Parameters
    ----------

    Return
    ------
    '''

    def __init__(self):

        '''
        '''

    def get_scores(forecaster, X_train, X_test, y_train, y_test, score):
        '''
        Returns in-sample and out-of-sample validation

        Parameters
        ----------

        score: string
        '''

        model = forecaster
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        return mape(y_test, y_pred)


if __name__ == '__main__':
    pass
