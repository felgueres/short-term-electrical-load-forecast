import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class pipeline (object):

    '''
    Clean, transform and handle missing values on dataset.

    Parameters
    ----------
    path: string
        Path to csv file.

    '''

    def __init__(self, path):

        # Load Dataframe from path.
        self.df = pd.read_csv(path)

    def transform(self):
        '''
        Set index, formatting and structure of dataframe.
        '''

        # Change names
        self.df.columns = ['full_date', 'kwh', 'temp', 'date', 'time', 'dow', 'month']

        # Set DatetimeIndex for easy time manipulation, set Frequency 15min.
        self.df.index = pd.DatetimeIndex(self.df.date) + pd.TimedeltaIndex(self.df.time)

        # Drop redundant columns.
        self.df.drop(['full_date','date','time'], axis = 1 , inplace = True)


    def fill_missing_temp(self):
        '''
        Fill missing temp values by time aware interpolation.
        '''

        # Time aware interpolation to fill missing values for temperature.
        self.df.temp = self.df.temp.interpolate(method = 'time')

    def fill_missing_kwh(self):
        '''
        Fill missing kwh values by time aware interpolation
        Note this data set only has 8 missing data points - 2 hours, hence its not worth spending more time in managing kwh missing values.
        '''

        self.df.kwh = self.df.kwh.interpolate(method = 'time')

    def fill_zeros_kwh(self):
        '''
        Replace kwh zero-values with dow mean for given month.
        Zero values in this context are not realistic, they are likely communication errors.
        '''

        # Get indeces for zero values.
        zero_indeces = a.df.ix[a.df.kwh == 0].index

        




    def dow_mean(self, dow, month, year):
        '''
        Returns mean of dow for given month/year to replace zero value entries.
        '''



        self.df.ix[a.df.kwh == 0].kwh.apply(lambda x: )



    def partition(self, start_date = datetime(2012,11,2,0,30), end_date = datetime(2013,12,1)):
        '''
        Partition dataset to analyis period.

        Parameters
        ----------

        start_date: datetime, default 2012/11/2
            Start of analysis period.

        end_date: datetime, default 2013/12/1
            End of analysis period.
        '''

        self.df = self.df[start_date:end_date]


    def clean(self):

        self.transform()
        self.fill_temp()
        self.fill_kwh()
        self.fixer()
        self.partition()

if __name__ == '__main__':
    pass
