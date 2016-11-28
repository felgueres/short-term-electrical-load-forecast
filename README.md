# load-forecast
Short-term load forecasting

Scope:

Forecast 24hr horizon electrical load at 15-min intervals.

Process overview:

1) Data Preprocessing and considerations

> (9) duplicated timestamps with NaN vals for kwh : dropped.

> 2013-08-17 - communication failure: replaced by period mean given dow/timestamp. Replacement period extended 24 hours to cover complete erroneous values.

> Temperature values - Time aware linear interpolation (polynomial could be considered).

> Given the units of kwh, data is considered to be consumption rather than power - ie. when aggregating to hourly values, was not converted to hourly values.

> methods:
    erroneous_kwh: Replace erroneous kwh entries (ie. zero) with dow-month mean. Has a tolerance timeframe to tackle erroneous data.

    [Show image of correction]

2) Build forecaster class

> Build model with:
    - Historical load
    - Temperature

> Tune model / parameters
> Weather forecast
> Extrapolate and forecast
