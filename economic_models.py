import numpy as np

def cobb_douglas_production(labor, capital, technology):
    """Cobb-Douglas production function"""
    alpha = 0.7  # Labor share
    return technology * (labor ** alpha) * (capital ** (1 - alpha))

def gini_coefficient(wealths):
    """Calculate the Gini coefficient of a wealth distribution"""
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / (len(cum_wealths) - 1)
    return (np.trapz(xarray, cum_wealths) / sum_wealths) / 0.5

def lorenz_curve(wealths):
    """Calculate the Lorenz curve of a wealth distribution"""
    sorted_wealths = np.sort(wealths)
    cum_wealths = np.cumsum(sorted_wealths)
    return np.insert(cum_wealths, 0, 0) / cum_wealths[-1]