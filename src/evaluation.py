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
        self.forecaster = forecaster
        self.y_pred = None

    def get_scores(self, score_metric):
        '''
        Returns test score.

        Parameters
        ----------

        score_metric: function
            Function to output model performance.

        Returns:
            Model score, float
        '''

        #Train test set.
        self.forecaster.model.fit(self.forecaster.X_train, self.forecaster.y_train)

        #Predict response.
        self.y_pred = self.forecaster.model.predict(self.forecaster.X_test)

        #Return score
        print 'The MAPE for this model is: ', score_metric(self.forecaster.y_test, self.y_pred)

if __name__ == '__main__':
    pass
