import numpy as np

def mape(y_true, y_pred):
    """
    Returns Mean Absolute Percentage Error
    """

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

if __name__ == '__main__':
    pass
