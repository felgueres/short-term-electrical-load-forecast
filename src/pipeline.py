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

    '''
    --------------------------------
    Section I : Clean-Transform-Fill
    '''

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

        # Date columns
        self.df['date'] = self.df.index.date


    def fill_missing_temp(self):
        '''
        Fill missing temp values by time aware interpolation.
        Returns
        -------
        self
        '''

        # Time aware interpolation to fill missing values for temperature.
        self.df.temp = self.df.temp.interpolate(method = 'time')

    def dropper(self):
        '''
        Drop duplicated rows (happen to be kWh == NaN), year, datecolumns.

        Returns
        -------
        self
        '''
        self.df.dropna(inplace = True)
        self.df.drop(['year','date'], axis=1, inplace = True)

    def erroneous_kwh(self, failure_timeframe = timedelta(hours = 48), failure_type = 0):
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

    def valid_period(self, start_date = datetime(2012,11,2,0,30), end_date = datetime(2013,11,30,23,45)):
        '''
        Partition dataset to valid period only.

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

    '''
    ---------------------------
    Section II: Create features
    '''

    def _features_d(self):
        '''
        Create features:
        - min temp values for day d
        - max temp values for day d

        '''
        # Generate min/max daily values.
        gb = self.df.resample('1D').temp
        gb = gb.agg(['min','max'])
        gb=gb.rename(columns = {'min':'min_temp_d', 'max':'max_temp_d' })

        # Create date feature to merge both dateframes.
        gb['date'] = gb.index.date

        # Merge features.
        self.df = self.df.reset_index().merge(gb, on ='date', how ='left').set_index('index')

    def _features_d_minus_1(self):
        '''
        Create features:
        - load of day d-1 at time interval h
        - morning load peak of d-1
        - evening load peak of d-1
        '''
        # Create load minus 1 day kwh feature.

        self.df['kwh_d_minus_1'] =  self.df.kwh.shift(96) #96 15-min intervals

        # Create load minus 1 day morning peak and afternoon peak.

        morning_max_d_minus = np.in1d(self.df.index.hour, np.array([7,8,9,10]))
        evening_max_d_minus = np.in1d(self.df.index.hour, np.array([11,12,13,14,15,16,17,18]))

        masks = [morning_max_d_minus,evening_max_d_minus]

        # Generate max morning day - 1 values.

        for i, mask in enumerate(masks):

            gb = self.df[mask].resample('1D').kwh_d_minus_1
            gb = gb.agg(['max'])
            gb=gb.rename(columns = {'max':'%d'%i})
            gb['date'] = gb.index.date

            # Merge features morning feature.
            self.df = self.df.reset_index().merge(gb, on ='date', how ='left').set_index('index')

        self.df = self.df.rename(columns = {'0':'morning_max_d_minus', '1':'evening_max_d_minus'})

    '''
    ---------------------------
    Section III: Run Pre-processing scripts and partition training-test set.
    '''

    def clean(self):
        '''
        Pre-processing of data.
        '''
        self.transform()
        self.fill_missing_temp()
        self.erroneous_kwh()
        self.valid_period()
        self._features_d()
        self._features_d_minus_1()
        self.dropper()

    def training_test_partition(self):

        '''
        Generate train-test set.
        Proper way to do this would be randomly divide the dataset into 

        Output
        ------

        train: csv file
            All dataset minus last 2-weeks of dataset.

        test: csv file
            Last 2-weeks of dataset.
        '''

        train_start_date = datetime(2012,11,2,0,30)
        train_end_date = datetime(2013,11,15,23,45)

        test_start_date = datetime(2013,11,16,0,0)
        test_end_date = datetime(2013,11,30,23,45)

        self.df[train_start_date:train_end_date].to_csv('../data/train_cleaned.csv')
        self.df[test_start_date:test_end_date].to_csv('../data/test_cleaned.csv')


if __name__ == '__main__':
    pass
