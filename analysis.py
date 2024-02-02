# Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings

##### EU Pollutant Time Series Analysis ############

def load_data(file_path):

    return pd.read_csv(file_path)

def select_eu_data(df, country='EU', indicator='Particulates (PM2.5)'):
    """
    Select and prepare the PM2.5 data for the EU.
    """
    pm25_eu = df[(df['Country'] == country) & (df['Indicator'] == indicator)]
    pm25_eu = pm25_eu.drop(columns=['Country', 'Indicator']).transpose()
    pm25_eu.reset_index(inplace=True)
    pm25_eu.columns = ['Year', 'PM2.5 Levels']
    pm25_eu['Year'] = pd.to_datetime(pm25_eu['Year'])
    return pm25_eu

def plot_time_series(data, title, y_label, window=5):
    """
    Plot the time series and a 5 year moving average.
    """
    sns.set_style("whitegrid")
    data['Moving Average'] = data['PM2.5 Levels'].rolling(window=window).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(data['Year'], data['PM2.5 Levels'], marker='o', label='Annual Levels', color='b')
    plt.plot(data['Year'], data['Moving Average'], marker='x', label=f'{window}-Year Moving Average', color='r')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def check_stationarity(time_series):
    """
    Perform the ADF test to check the stationarity of the time series.
    """
    result = adfuller(time_series)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    return result[1] <= 0.05

def fit_arima_model(time_series, order):
    """
    Fit an ARIMA model to the time series data.
    """
    model = ARIMA(time_series, order=order)
    model_fit = model.fit()
    print(model_fit.summary())
    return model_fit

def forecast_arima(model_fit, periods):
    """
    Forecast future values using the fitted ARIMA model.
    """
    forecast = model_fit.forecast(steps=periods)
    return forecast

def run_analysis(file_path, country='EU', indicator='Particulates (PM2.5)', arima_order=(1, 1, 1), forecast_periods=5):
    """
    Run the entire analysis pipeline.
    """
    # Load and prepare data
    df = load_data(file_path)
    pm25_eu = select_eu_data(df, country, indicator)

    # Plot time series
    plot_time_series(pm25_eu, f'Time Series of {indicator} Levels for {country}', 'PM2.5 Levels')

    # Check for stationarity and fit ARIMA model if stationary
    if check_stationarity(pm25_eu['PM2.5 Levels']):
        model_fit = fit_arima_model(pm25_eu['PM2.5 Levels'], arima_order)
        # Forecast future values
        future_forecast = forecast_arima(model_fit, forecast_periods)
        print(f'Future Forecast for {forecast_periods} periods:', future_forecast)

# Running the analysis
file_path = '/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data/air_pol.csv' 
run_analysis(file_path)

######## China - Regressed Health Exp on CO2 Emissions ##############

import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression

def load_and_filter_data(co2_file_path, health_exp_file_path, country):

    co2_df = pd.read_csv(co2_file_path)
    health_exp_df = pd.read_csv(health_exp_file_path)

    # Filtering data for the specified country
    co2_country = co2_df[co2_df['Country'] == country].iloc[:, 1:-1]
    health_exp_country = health_exp_df[health_exp_df['Country'] == country].iloc[:, 2:]

    return co2_country, health_exp_country

def align_datasets(co2_data, health_exp_data):

    common_years = co2_data.columns.intersection(health_exp_data.columns).tolist()
    co2_aligned = co2_data[common_years].iloc[0].astype(float)
    health_exp_aligned = health_exp_data[common_years].iloc[0].astype(float)

    return co2_aligned, health_exp_aligned, common_years

def perform_regression_analysis(X, y):
    """
    Perform linear regression analysis.

    """
    reg_model = LinearRegression()
    reg_model.fit(X, y)
    intercept = reg_model.intercept_
    slope = reg_model.coef_[0]
    r_squared = reg_model.score(X, y)

    return intercept, slope, r_squared

def analyze_co2_health_expenditure_relationship(co2_file_path, health_exp_file_path, country):

    # Load and filter data
    co2_data, health_exp_data = load_and_filter_data(co2_file_path, health_exp_file_path, country)

    # Align datasets
    co2_aligned, health_exp_aligned, common_years = align_datasets(co2_data, health_exp_data)

    # Prepare data for regression
    X = co2_aligned.values.reshape(-1, 1)
    y = health_exp_aligned.values

    # Perform regression analysis
    intercept, slope, r_squared = perform_regression_analysis(X, y)

    return intercept, slope, r_squared, common_years

# Path to the datasets
co2_file_path = '/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data/CO2_emissions.csv'
health_exp_file_path = '/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data/health_exp.csv'
country = "China"

# Call the function to perform the analysis
analyze_co2_health_expenditure_relationship(co2_file_path, health_exp_file_path, country)

