# Short-term load forecasting

## Scope:

### Forecast 24hr horizon electrical load at 15-min intervals.

Process overview:

1) Data Preprocessing

- Temperature values - Time aware linear interpolation (the best idea would be to do a 2 variable interpolation load-temp)

2) Build forecaster class

> Build model with:
    - Historical load
    - Temperature

> Tune model / parameters
> Weather forecast
> Extrapolate and forecast
