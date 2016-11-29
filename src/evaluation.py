import numpy as np

class evaluation(object):
    '''
    Produce evaluation metrics.

    Parameters
    ----------

    Return
    ------
    '''

    def __init__(self, score):
        '''

        '''


    def evaluate(self):
        '''
        Returns in-sample and out-of-sample validation


        Parameters
        ----------

        score: string
        '''


def MAPE(y_true, y_pred):
    """
    Returns Mean Absolute Percentage Error
    """

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


if __name__ == '__main__':
    pass
