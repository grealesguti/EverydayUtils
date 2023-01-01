import argparse
import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import curves

def find_best_single_fit(filename, curve_type):
    x = []
    y = []

    # Read the data from the CSV file
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x.append(float(row[0]))
            y.append(float(row[1]))

    # Define a function to fit the data to
    def func(x, a, b, c):
        if curve_type == 'exponential':
            return a * np.exp(-b * x) + c
        elif curve_type == 'linear':
            return a * x + b
        elif curve_type == 'quadratic':
            return a * x**2 + b * x + c
        else:
            raise ValueError('Invalid curve type')

    # Fit the curve to the data
    params, params_covariance = curve_fit(func, x, y)

    return params
    
def find_best_overall_fit(x, y):
    best_fit_params = None
    best_fit_type = None
    best_fit_error = float('inf')
    for curve_func, curve_type in zip(curves.CURVE_FUNCS, curves.CURVE_TYPES):
        try:
            params, params_covariance = curve_fit(curve_func, x, y)
            y_pred = curve_func(x, *params)
            error = np.mean((y - y_pred)**2)
            if error < best_fit_error:
                best_fit_params = params
                best_fit_type = curve_type
                best_fit_error = error
        except:
            pass  # curve fit failed

    return best_fit_params, best_fit_type


def parse_args():
    parser = argparse.ArgumentParser(description='Find the best fit curve for a series of data in a CSV file')
    parser.add_argument('filename', type=str, help='The CSV file containing the data')
    parser.add_argument('--curve-type', type=str, default='exponential', choices=['exponential', 'linear', 'quadratic'], help='The type of curve to fit the data to')
    return parser.parse_args()

def plot_best_fit(x, y, params, curve_type):
    plt.scatter(x, y)

    if curve_type in curves.CURVE_TYPES:
        index = curves.CURVE_TYPES.index(curve_type)
        func = curves.CURVE_FUNCS[index]
    else:
        raise ValueError('Invalid curve type')

    x_range = np.linspace(min(x), max(x), 1000)
    y_pred = func(x_range, *params)
    plt.plot(x_range, y_pred)
    plt.show()


if __name__ == '__main__':
    args = parse_args()
    params = find_best_fit(args.filename, args.curve_type)
    print(params)

