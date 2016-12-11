# Short-term load forecasting

## Scope:

### Forecast 24hr horizon electrical load at 15-min intervals.

Overview:

### 1) Data Preprocessing

-   Filled in missing values for temperature:

        Time-aware linear interpolation

-   Fixed erroneous load data:

        Replaced zero values with day-of-week / month mean for specific interval.

-   Dataset partitioning:

        Divided data in a) training-validation and, b) test set

### 2) Model Formulation

-   EDA:

        Explored relationship of time - temperature - load

![alt tag] (https://github.com/felgueres/load-forecast/blob/master/figures/01-EDA-temp-load-relationship.png)

-   Model Selection:

        Random Forest -- Perform good with non-linear data, easy tuning (given time constraint) and implementation, scalable for this application.

        Working hypothesis about the model: Multiple independent models perform better than an aggregate since long-term exposure would introduce trend bias.

-   Feature creation:

        Temporal features (ie. previous day interval, morning / afternoon peak, min / max temperature)

### 3) Model tuning

-   Built methodology to cross-validate

        See notebooks/02 for details.

### 4) Test model

-   Evaluation class

        Takes forecaster class and test set as parameter for out-of-sample validation.

        Used Mean Absolute Percentage Error

-   Sample out-of-sample prediction: MAPE = 1.8 % 

![alt tag] (https://github.com/felgueres/load-forecast/blob/master/figures/02-One-Day-Forecast.png)

### 5) Ongoing thoughts

-   Still high variance, cross-validate features, tree parameters, increase robustness of special days.

-   Temperature should be estimated through 2 variable interpolation of load-temperature.

-   Explain static load on weekdays.
