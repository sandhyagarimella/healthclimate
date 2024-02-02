import os
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt

# Data Loading Function
def load_dataframes(base_path, file_names):
    dataframes = {}
    for file_name in file_names:
        full_path = os.path.join(base_path, file_name)
        try:
            dataframes[file_name] = pd.read_csv(full_path)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    return dataframes

# Usage
PATH = r'/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data'
file_list = [
    'china_mean_lst.csv',
    'europe_mean_lst.csv',
    'climate_disasters_frequency.csv',
    'CO2_emissions.csv',
    'protection_exp.csv',
    'env_taxes.csv',
    'resp.csv',
    'health_exp.csv',
    'com_disease.csv',
    'air_pol.csv'
]

dataframes = load_dataframes(PATH, file_list)
climate_disasters = dataframes.get('climate_disasters_frequency.csv')
CO2_emissions = dataframes.get('CO2_emissions.csv')


def create_climate_disasters_plot(dataframe, country1, country2):
    # Filtering data for country
    filtered_disasters = dataframe[dataframe['Country'].isin([country1, country2])]

    # Converting to long format for plotting
    filtered_disasters_long = filtered_disasters.melt(id_vars=['Country', 'Indicator'], var_name='Year', value_name='Value')
    filtered_disasters_long['Year'] = filtered_disasters_long['Year'].str[-2:]

    # Plotting
    plt.figure(figsize=(15, 6))
    for name, group in filtered_disasters_long.groupby('Country'):
        plt.plot(group['Year'], group['Value'], label=name)

    plt.title(f'Climate Disasters Over Years in {country1} and {country2}')
    plt.xlabel('Year')
    plt.ylabel('Number of Disasters')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)



def create_co2_emissions_plot(dataframe, country1, country2):
    # Extracting data for the selected countries
    country1_data = dataframe[dataframe['Country'] == country1].iloc[:, 1:-1].transpose()
    country1_data.columns = [country1]

    country2_data = dataframe[dataframe['Country'] == country2].iloc[:, 1:-1].transpose()
    country2_data.columns = [country2]

    # Combining the data
    combined_data = pd.concat([country1_data, country2_data], axis=1)

    # Creating the plot
    years = combined_data.index
    short_years = [year[-2:] for year in years]

    plt.figure(figsize=(12, 6))
    plt.plot(combined_data, marker='o')
    plt.title(f'Emissions of {country1} and {country2} Over Years')
    plt.xlabel('Year')
    plt.ylabel('Emissions (millions of metric tons of CO2)')
    plt.xticks(ticks=range(len(years)), labels=short_years)
    plt.legend(combined_data.columns)
    plt.grid(True)


# Shiny App Code
app_ui = ui.page_fluid(
    ui.panel_title("Interactive Plots - Health and Climate"),
    # UI for selecting countries
    ui.input_select(id='country1_disasters', label='Choose first country for Climate Disasters', choices=['China', 'EU']),
    ui.input_select(id='country2_disasters', label='Choose second country for Climate Disasters', choices=['China', 'EU']),
    ui.output_plot(id='climate_disasters_plot'),
    ui.input_select(id='country1_co2', label='Choose first country for CO2 Emissions', choices=['China', 'EU']),
    ui.input_select(id='country2_co2', label='Choose second country for CO2 Emissions', choices=['China', 'EU']),
    ui.output_plot(id='co2_emissions_plot')
)

def server(input, output, session):
    @reactive.Calc
    def get_climate_data():
        country1 = input.country1_disasters()
        country2 = input.country2_disasters()
        return create_climate_disasters_plot(climate_disasters, country1, country2)

    @reactive.Calc
    def get_co2_data():
        country1 = input.country1_co2()
        country2 = input.country2_co2()
        return create_co2_emissions_plot(CO2_emissions, country1, country2)

    @output
    @render.plot
    def climate_disasters_plot():
        country1 = input.country1_disasters()
        country2 = input.country2_disasters()
        create_climate_disasters_plot(climate_disasters, country1, country2)

    @output
    @render.plot
    def co2_emissions_plot():
        country1 = input.country1_co2()
        country2 = input.country2_co2()
        create_co2_emissions_plot(CO2_emissions, country1, country2)

app = App(app_ui, server)
