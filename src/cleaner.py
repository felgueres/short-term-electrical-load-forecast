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
        Returns
        -------
        self
        '''
        # Change names
        self.df.columns = ['full_date', 'kwh', 'temp', 'date', 'time', 'dow', 'month']

        # Set DatetimeIndex for easy time manipulation, set Frequency 15min.
        self.df.index = pd.DatetimeIndex(self.df.date) + pd.TimedeltaIndex(self.df.time)

        # Drop redundant columns.
        self.df.drop(['full_date','date','time'], axis = 1 , inplace = True)

        # Create int based time - 1 day : 96 15-min intervals
        self.df['interval'] = (self.df.index.hour * 4) + (self.df.index.minute /15) # TODO use resample or pandas func to replace hard coded numbers.

        # Year column
        self.df['year'] =  self.df.index.year

    def fill_missing_temp(self):
        '''
        Fill missing temp values by time aware interpolation.
        Returns
        -------
        self
        '''

        # Time aware interpolation to fill missing values for temperature.
        self.df.temp = self.df.temp.interpolate(method = 'time')

    def drop_duplicates(self):
        '''
        Drop duplicated rows (happen to be kWh == NaN)

        Returns
        -------
        self
        '''
        self.df.kwh.dropna(axis= 0, inplace = True)

    def erroneous_kwh(self, failure_timeframe = timedelta(hours = 12), failure_type = 0):
        '''
        Replace erroneous entries with dow-month mean.
        Zero values in this context are not realistic, they are likely communication errors.

        Parameters
        ----------

        failure_timeframe: timedelta, default = timedelta(hours =1)
            Specify the tolerance timeframe to discard erroneous data.

        failure_type: int, default = 0
            Specify considerations for erroneous data.
            TODO: Expand for complex failure detection.

        Returns
        -------
        self
        '''

        # Get indeces for zero values.
        zero_vals = self.df.ix[(self.df.kwh == failure_type)].index

        # Timeframe to discard erroneous data.
        indeces_min = zero_vals.min() - failure_timeframe
        indeces_max = zero_vals.max() + failure_timeframe

        time_index = pd.DatetimeIndex(start = indeces_min, end = indeces_max, freq = '15T')

        # Replace values with dow mean.
        for ts in time_index:
            event = self.df.loc[ts]
            self.df.loc[ts,'kwh'] = self.dow_mean(event.dow, event.month, event.year, event.interval, time_index)

    def dow_mean(self, dow, month, year, interval, time_index):
        '''
        Returns mean of dow for given month/year.

        Parameters
        ----------
        dow: int
            Event day of week.
        month: int
            Event month.
        year: int
            Event year.
        interval: int
            Daily interval (0-95).
        time_index: DatetimeIndex
            Failure timeframe to be exlcuded from mean.

        Returns
        -------
        dow_mean: float
            Mean of this dow fiven month and year.
        '''


        _df = self.df.loc[-self.df.index.isin(time_index)] # Note we want the inverse of isin, hence the minus sign.

        return _df.ix[(_df.dow == dow)&
                            (_df.month == month)&
                            (_df.year == year)&
                            (_df.interval == interval)].kwh.mean(axis=0)

    def partition(self, start_date = datetime(2012,11,2,0,30), end_date = datetime(2013,12,1)):
        '''
        Partition dataset to analyis period.
        Parameters
        ----------
        start_date: datetime, default 2012/11/2
            Start of analysis period.

        end_date: datetime, default 2013/12/1
            End of analysis period.

        Returns
        -------
        self
        '''

        self.df = self.df[start_date:end_date]


    def clean(self):

        self.transform()
        self.fill_missing_temp()
        self.erroneous_kwh()
        self.partition()
        self.drop_duplicates()


if __name__ == '__main__':
    pass
