# Plotting

import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to load dataframes
def load_dataframes(base_path, file_names):
    dataframes = {}
    for file_name in file_names:
        full_path = os.path.join(base_path, file_name)
        try:
            dataframes[file_name] = pd.read_csv(full_path)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    return dataframes

# Function to restructure a dataframe for time series analysis
def restructure_df(df):
    df_long = df.melt(id_vars=['Country', 'Indicator'], var_name='Year', value_name='Value')
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    df_long = df_long.dropna(subset=['Year'])
    df_pivot = df_long.pivot_table(index=['Country', 'Year'], columns='Indicator', values='Value').reset_index()
    return df_pivot

# Function to plot time series data
def plot_time_series(data, x_col, y_col, title, x_label, y_label):
    plt.figure(figsize=(10, 5))
    plt.plot(data[x_col], data[y_col], marker='o', color='blue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def main():
    # Define paths and file names
    base_path = r'/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data'
    file_list = [
        'env_taxes.csv',
        'resp.csv',
        'eu_combined_df.csv',
        'air_pol.csv'
    ]

    # Load dataframes
    dataframes = load_dataframes(base_path, file_list)

    # Access dataframes using the correct file names
    environment_taxes = dataframes.get('env_taxes.csv')
    mortality = dataframes.get('resp.csv')

    # Static Plots
    ########### COMPARISON OF ENVIRONMENTAL TAXES AS PERCENT OF GDP ##############
    data_df = environment_taxes

    china_data = data_df[data_df['Country'] == 'China']
    eu_data = data_df[data_df['Country'] == 'EU']

    china_long = china_data.melt(id_vars=['Country', 'Indicator'], var_name='Year', value_name='Value')
    eu_long = eu_data.melt(id_vars=['Country', 'Indicator'], var_name='Year', value_name='Value')

    combined_data = pd.concat([china_long, eu_long])

    combined_data['Year'] = combined_data['Year'].astype(str)
    combined_data['Year'] = combined_data['Year'].str[2:]

    plt.figure(figsize=(10, 6))
    for name, group in combined_data.groupby('Country'):
        plt.plot(group['Year'], group['Value'], label=name)

    plt.title('Environmental Taxes (as % of GDP) Over Years in China and EU')
    plt.xlabel('Year')
    plt.ylabel('Environmental Taxes (% of GDP)')
    plt.legend()
    plt.grid(True)
    plt.show()

    dataframes = load_dataframes(base_path, file_list)

    # Filter the EU dataframe for air pollution
    air_pol_df = dataframes.get('air_pol.csv')
    eu_air_pol = air_pol_df[air_pol_df['Country'] == 'EU']

    # Plotting the time series for each pollutant in the EU data
    pollutants = eu_air_pol['Indicator'].unique()
    plt.figure(figsize=(10, 6))
    for pollutant in pollutants:
        pollutant_data = eu_air_pol[eu_air_pol['Indicator'] == pollutant]
        years = [int(year) for year in pollutant_data.columns[2:]]
        values = pollutant_data.iloc[0, 2:]
        plt.plot(years, values, label=pollutant)

    plt.title('Air Pollution Over Time in the EU')
    plt.xlabel('Year')
    plt.ylabel('Pollution Level')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
