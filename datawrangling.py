# Data Wrangling

import pandas as pd
import os
import requests

PATH = r'/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data'

# Define your file names
file_names = [
    "BERKELEY_chinameanlst.txt",
    "BERKELEY_europemeanlst.txt",
    "IMF_Climate-related_Disasters_Frequency.csv",
    "IMF_CO2_Emissions_Intensities_Multipliers.csv",
    "IMF_Environmental_Protection_Expenditures.csv",
    "IMF_Environmental_Taxes.csv",
    "OECD_ Mortality_due_to_Respiratory_Illness.csv",
    "OECD_Healthcare_Expenditure.csv",
    "OECD_Incidence_of_Communicable_Diseases.csv"
]

pollution_data_url = "https://stats.oecd.org/SDMX-JSON/data/AIR_EMISSIONS/FRA+DEU+ITA+POL+ESP.SOX+NOX+PM10+PM2-5+CO+NMVOC.INTENSITY+TOT_CAP/all?startTime=1990&endTime=2021"
fetch_from_web = True
pollution_data_filename = "pollution_data.csv" 

fname = "BERKELEY_chinameanlst.txt"
fname2 = "BERKELEY_europemeanlst.txt"
fname3 = "IMF_Climate-related_Disasters_Frequency.csv"
fname4 = "IMF_CO2_Emissions_Intensities_Multipliers.csv"
fname5 = "IMF_Environmental_Protection_Expenditures.csv"
fname6 = "IMF_Environmental_Taxes.csv"
fname7 = "OECD_ Mortality_due_to_Respiratory_Illness.csv"
fname8 = "OECD_Healthcare_Expenditure.csv"
fname9 = "OECD_Incidence_of_Communicable_Diseases.csv"
local_file = "local_pollution_data.json"


# The functions load_fname and load_fname2 pull up the mean land surface temperatures of china and europe
# respectively. The temperatures are in Celsius and reported as anomalies relative to the Jan 1951-
# Dec 1980 average of 8.15 +/- 0.12. Only the annual anomaly and annual uncertainty data in June are retained 
# since the measurements are monthly and the annual average of a year is reported in June.



def load_fname(path, fname):

    file_path = os.path.join(PATH, fname)
    with open(file_path, 'r') as file:
        lines = file.readlines()[68:]

    df = pd.DataFrame([line.strip().split() for line in lines])

    df.iloc[0] = ['-', '-', 'monthly', 'monthly', 'annual', 'annual', 'five-year', 'five-year', 
                  'ten-year', 'ten-year', 'twenty-year', 'twenty-year', None]
    df.iloc[1] = ['year', 'month', 'anomaly', 'unc.', 'anomaly', 'unc.', 'anomaly', 'unc.', 
                  'anomaly', 'unc.', 'anomaly', 'unc.', None]

    df.drop(columns=df.columns[12], inplace=True) 
    df.dropna(how='all', inplace=True)
    df = df[df[0] != 'year']
    
    row_to_modify = df[df[0] == '-'].index[0]
    new_row_values = ["year", "month", "monthly anomaly", "monthly unc.",
        "annual anomaly", "annual unc.", "five-year anomaly", "five-year unc.",
        "ten-year anomaly", "ten-year unc.", "twenty-year anomaly", "twenty-year unc."]
    
    df.iloc[row_to_modify] = new_row_values
    
    new_header = df.iloc[0]  
    df = df[1:]  
    df.columns = new_header
    
    df['year'] = pd.to_numeric(df['year'])
    df['month'] = pd.to_numeric(df['month'])

    df = df[df['month'] == 6]
    
    columns_to_keep = ['year', 'annual anomaly', 'annual unc.']
    df = df[columns_to_keep]
    
    df.reset_index(drop=True, inplace=True)
    
    anomaly_pivot = df.pivot_table(index=lambda x: 'Annual Anomaly', columns='year', values='annual anomaly')
    
    unc_pivot = df.pivot_table(index=lambda x: 'Annual Uncertainty', columns='year', values='annual unc.')
    
    final_pivot = pd.concat([anomaly_pivot, unc_pivot])
    
    final_pivot = final_pivot.rename(columns={'Variable': 'Indicator'})
    
    final_pivot['Country'] = 'China'
    
    final_pivot['Indicator'] = ['LST Annual Anomaly', 'LST Annual Uncertainty']

    return final_pivot

##########################################################

def load_fname2(path, fname2):
    file_path2 = os.path.join(PATH, fname2)    
    with open(file_path2, 'r') as file:
        lines = file.readlines()[68:]

    df = pd.DataFrame([line.strip().split() for line in lines])

    df.iloc[0] = ['-', '-', 'monthly', 'monthly', 'annual', 'annual', 'five-year', 'five-year', 'ten-year', 'ten-year', 'twenty-year', 'twenty-year', None]
    df.iloc[1] = ['year', 'month', 'anomaly', 'unc.', 'anomaly', 'unc.', 'anomaly', 'unc.', 'anomaly', 'unc.', 'anomaly', 'unc.', None]

    df.drop(columns=df.columns[12], inplace=True)
    
    df.dropna(how='all', inplace=True)
    df = df[df[0] != 'year']
    
    row_to_modify = df[df[0] == '-'].index[0]
    new_row_values = ["year", "month", "monthly anomaly", "monthly unc.",
        "annual anomaly", "annual unc.", "five-year anomaly", "five-year unc.",
        "ten-year anomaly", "ten-year unc.", "twenty-year anomaly", "twenty-year unc."]
    
    df.iloc[row_to_modify] = new_row_values
    
    new_header = df.iloc[0] 
    df = df[1:]  
    df.columns = new_header
    
    df['year'] = pd.to_numeric(df['year'])
    df['month'] = pd.to_numeric(df['month'])
    
    df = df[df['month'] == 6]
    
    columns_to_keep = ['year', 'annual anomaly', 'annual unc.']
    df = df[columns_to_keep]
    
    df.reset_index(drop=True, inplace=True)

    anomaly_pivot = df.pivot_table(index=lambda x: 'Annual Anomaly', columns='year', values='annual anomaly')
    
    unc_pivot = df.pivot_table(index=lambda x: 'Annual Uncertainty', columns='year', values='annual unc.')
    
    final_pivot = pd.concat([anomaly_pivot, unc_pivot])
    
    final_pivot = final_pivot.rename(columns={'Variable': 'Indicator'})
    
    final_pivot['Country'] = 'EU'
    
    final_pivot['Indicator'] = ['LST Annual Anomaly', 'LST Annual Uncertainty']

    return final_pivot     

###############################################################

def load_fname3(path, fname3):

    df = pd.read_csv(os.path.join(PATH, fname3))

    countries_to_keep = ["China, P.R.: Hong Kong",
        "China, P.R.: Macao",
        "China, P.R.: Mainland",
        "Germany",
        "Germany Dem Rep (former)",
        "Germany Fed Rep (former)",
        "France",
        "Spain",
        "Italy",
        "Poland, Rep. of"]

    df = df[df['Country'].isin(countries_to_keep)]

    return df

climate_disasters_frequency = load_fname3(PATH, fname3)
climate_disasters_frequency.head


def clean_fname3(df):

    columns_to_keep = ["ObjectId", "Country", "Indicator"] + [f"F{year}" for year in range(1980, 2023)]

    df = df[columns_to_keep]

    indicator_value = "Climate related disasters frequency, Number of Disasters: TOTAL"
    df = df[df["Indicator"] == indicator_value]
    
    china_data = df[df['Country'].str.contains("China")].iloc[:, 3:].sum()
    germany_data = df[df['Country'] == "Germany"].iloc[:, 3:].sum()
    
    df.columns = [col[1:] if col.startswith('F') else col for col in df.columns]
    
    selected_countries = ['France', 'Italy', 'Poland, Rep. of', 'Spain']
    selected_countries_df = df[df['Country'].isin(selected_countries)]
    china_row = pd.DataFrame([[None, 'China', None] + china_data.tolist()], columns=df.columns)
    germany_row = pd.DataFrame([[None, 'Germany', None] + germany_data.tolist()], columns=df.columns)

    combined_df = pd.concat([selected_countries_df, china_row, germany_row], ignore_index=True)
    
    combined_df['Indicator'] = "Climate related disasters frequency, Number of Disasters: TOTAL"
    
    eu_countries = ['Germany', 'Italy', 'France', 'Spain', 'Poland, Rep. of']
    
    eu_sum = combined_df[combined_df['Country'].isin(eu_countries)].iloc[:, 3:].sum()
    
    eu_row = pd.DataFrame([{'Country': 'EU', 'Indicator': df['Indicator'].iloc[0]}])
    for col in combined_df.columns[3:]:
        eu_row[col] = eu_sum[col]
    
    df_with_eu = pd.concat([combined_df, eu_row], ignore_index=True)
    
    return df_with_eu

#############################################################


def load_fname4(path, fname4):

    df = pd.read_csv(os.path.join(path, fname4))

    countries_to_keep = ["China, P.R.: Hong Kong",
                         "China, P.R.: Macao",
                         "China, P.R.: Mainland",
                         "Germany",
                         "Germany Dem Rep (former)",
                         "Germany Fed Rep (former)",
                         "France",
                         "Spain",
                         "Italy",
                         "Poland, Rep. of"]

    df = df[df['Country'].isin(countries_to_keep)]
    df = df[df['CTS_Name'] == 'CO2 Emissions']
    
    columns_to_keep = ["ObjectId", "Country", "Indicator"] + [f"F{year}" for year in range(1995, 2019)]

    df = df[columns_to_keep]

    return df

# Load the data using the function
CO2_emissions = load_fname4(PATH, fname4)

def clean_fname4(df):

    countries_of_interest = ['China', 'Germany', 'France', 'Italy', 'Spain', 'Poland']

    indicator_df = pd.DataFrame({'Indicator': ['CO2 Emissions']})

    final_emissions = pd.DataFrame(index=countries_of_interest)

    for year in range(1995, 2019):
        column_name = f'F{year}'
        year_sums = []

        for country in countries_of_interest:
            filtered_df = CO2_emissions[CO2_emissions['Country'].str.contains(country)]

            sum_values = filtered_df[column_name].sum()
            year_sums.append(sum_values)

        final_emissions[column_name] = year_sums

    final_emissions.reset_index(inplace=True)
    final_emissions.rename(columns={'index': 'Country'}, inplace=True)

    final_emissions = final_emissions.merge(indicator_df, how='cross')

    final_emissions.columns = [col[1:] if col.startswith('F') else col for col in final_emissions.columns]

    eu_countries = ['Poland', 'Italy', 'Spain', 'Germany', 'France']
    
    eu_sum = final_emissions[final_emissions['Country'].isin(eu_countries)].iloc[:, 3:].sum()
    
    eu_row = pd.DataFrame([eu_sum], index=["EU"])
    eu_row.insert(0, 'Country', 'EU')
    
    indicator_value = final_emissions[final_emissions['Country'] == 'France']['Indicator'].iloc[0]
    eu_row['Indicator'] = indicator_value
    
    df_with_eu = pd.concat([final_emissions, eu_row], ignore_index=True)

    return df_with_eu

###############################################################

def load_fname5(path, fname5):

    df = pd.read_csv(os.path.join(PATH, fname5))

    df = df[df['Unit'] == "Percent of GDP"]

    countries_to_keep = ["China, P.R.: Hong Kong",
        "China, P.R.: Macao",
        "China, P.R.: Mainland",
        "Germany",
        "Germany Dem Rep (former)",
        "Germany Fed Rep (former)",
        "France",
        "Spain",
        "Italy",
        "Poland, Rep. of"]

    df = df[df['Country'].isin(countries_to_keep)]
    
    columns_to_keep = ["ObjectId", "Country", "Indicator"] + [f"F{year}" for year in range(1995, 2022)]

    df = df[columns_to_keep]

    return df


def clean_fname5(df):
    countries_of_interest = ['China', 'Germany', 'France', 'Italy', 'Spain', 'Poland']

    final_protection_exp = pd.DataFrame(index=countries_of_interest)
    
    indicator_value = df['Indicator'].iloc[0]

    for year in range(1995, 2022):
        column_name = f'F{year}'
        year_sums = []

        for country in countries_of_interest:
            filtered_df = df[df['Country'].str.contains(country)]

            sum_values = filtered_df[column_name].sum()
            year_sums.append(sum_values)

        final_protection_exp[column_name] = year_sums

    final_protection_exp.reset_index(inplace=True)
    final_protection_exp.rename(columns={'index': 'Country'}, inplace=True)
    
    final_protection_exp.columns = [col[1:] if col.startswith('F') else col for col in final_protection_exp.columns]

    final_protection_exp['Indicator'] = indicator_value

    eu_countries = ['Germany', 'Italy', 'France', 'Spain', 'Poland']
    
    eu_row = {'Country': 'EU'}
    
    for year in range(1995, 2022):
        column_name = str(year)
        eu_row[column_name] = final_protection_exp[final_protection_exp['Country'].isin(eu_countries)][column_name].mean()
    
    df_with_eu = final_protection_exp.append(eu_row, ignore_index=True)
    df_with_eu.loc[df_with_eu['Country'] == 'EU', 'Indicator'] = "Expenditure on biodiversity and landscape protection"

    return df_with_eu


################################################################


def load_fname6(path, fname6):

    df = pd.read_csv(os.path.join(PATH, fname6))

    df = df[df['Unit'] == "Percent of GDP"]

    countries_to_keep = ["China, P.R.: Hong Kong",
        "China, P.R.: Macao",
        "China, P.R.: Mainland",
        "Germany",
        "Germany Dem Rep (former)",
        "Germany Fed Rep (former)",
        "France",
        "Spain",
        "Italy",
        "Poland, Rep. of"]

    df = df[df['Country'].isin(countries_to_keep)]
    
    columns_to_keep = ["ObjectId", "Country", "Indicator"] + [f"F{year}" for year in range(1995, 2022)]

    df = df[columns_to_keep]
    
    df.columns = [col[1:] if col.startswith('F') else col for col in df.columns]

    return df

env_taxes = load_fname6(PATH, fname6)
env_taxes

def clean_fname6(df):

    countries_of_interest = ['China', 'Germany', 'France', 'Italy', 'Spain', 'Poland']
    final_df = pd.DataFrame(index=countries_of_interest)
    
    indicator_value = env_taxes['Indicator'].iloc[0]

    for year in range(1995, 2022): 
        column_name = f'{year}'
        year_sums = []

        for country in countries_of_interest:
            filtered_df = df[df['Country'].str.contains(country)]
            sum_values = filtered_df[column_name].sum()
            year_sums.append(sum_values)

        temp_df = pd.DataFrame({column_name: year_sums}, index=countries_of_interest)
        final_df = final_df.merge(temp_df, left_index=True, right_index=True, how='left')

    final_df.reset_index(inplace=True)
    final_df.rename(columns={'index': 'Country'}, inplace=True)
    
    final_df['Indicator'] = indicator_value

    eu_countries = ['Germany', 'Italy', 'France', 'Spain', 'Poland']
    
    eu_row = {'Country': 'EU'}
    
    for year in range(1995, 2022):
        column_name = str(year)
        eu_row[column_name] = final_df[final_df['Country'].isin(eu_countries)][column_name].mean()
    
    df_with_eu = final_df.append(eu_row, ignore_index=True)
    df_with_eu.loc[df_with_eu['Country'] == 'EU', 'Indicator'] = 'Environmental Taxes'

    return df_with_eu

#################################################################


def load_fname7(path, fname):
    df = pd.read_csv(os.path.join(path, fname))
    
    df = df[df['Variable'] == "Diseases of the respiratory system"]

    countries_to_keep = ["China", "Germany", "France", "Spain", "Italy", "Poland"]
    df = df[df['Country'].isin(countries_to_keep)]

    df = df[df['Measure'] == 'Deaths per 100 000 population (standardised rates)']

    columns_to_keep = ["Country", "Measure", "Year", "Value"] 
    df = df[columns_to_keep]
    
    pivoted_df = df.pivot_table(index=['Country', 'Measure'], columns='Year', values='Value')

    pivoted_df.reset_index(inplace=True)

    eu_countries = ['Germany', 'France', 'Italy', 'Spain', 'Poland']
    eu_df = df[df['Country'].isin(eu_countries)].groupby(['Measure', 'Year']).mean().reset_index()
    eu_df['Country'] = 'EU'
    eu_pivot = eu_df.pivot_table(index=['Country', 'Measure'], columns='Year', values='Value')
    eu_pivot.reset_index(inplace=True)

    final_df = pd.concat([pivoted_df, eu_pivot], ignore_index=True)
    final_df = final_df.rename(columns={'Measure': 'Indicator'})

    return final_df


############################################################


def load_fname8(path, fname):
    # Load the CSV file
    df = pd.read_csv(os.path.join(path, fname))

    df = df[df['Function'] == "Current expenditure on health (all functions)"]
    df = df[df['Measure'] == "Share of gross domestic product"]
    df = df[df['Financing scheme'] == "Government/compulsory schemes"]
    df = df[df['Provider'] == "All providers"]

    countries = ["China", "Germany", "France", "Spain", "Italy", "Poland"]
    
    pattern = '|'.join(countries)
    
    df = df[df['Country'].str.contains(pattern, na=False)]

    columns_to_keep = ["Country", "Function", "Year", "Value"] 
    df = df[columns_to_keep]
    
    pivoted_data = df.pivot_table(index=['Country', 'Function'], columns='Year', values='Value')
    
    pivoted_data.reset_index(inplace=True)
    
    eu_countries = ['Germany', 'Italy', 'Spain', 'France', 'Poland']
    
    eu_data = pivoted_data[pivoted_data['Country'].isin(eu_countries)]
    
    eu_mean = eu_data.groupby('Function').mean()
    
    eu_mean['Country'] = 'EU'
    
    eu_mean.reset_index(inplace=True)
    eu_mean = eu_mean[['Country', 'Function'] + [col for col in eu_mean.columns if col not in ['Country', 'Function']]]
    
    pivoted_data_with_eu = pd.concat([pivoted_data, eu_mean], ignore_index=True)
    
    pivoted_data_with_eu['Country'] = pivoted_data_with_eu['Country'].replace("China (People's Republic of)", "China")
    
    pivoted_data_with_eu = pivoted_data_with_eu.rename(columns={'Function': 'Indicator'})
    
    return pivoted_data_with_eu



###############################################################


def load_fname9(path, fname):

    df = pd.read_csv(os.path.join(PATH, fname9))
    df = df[df['Measure'] == "Incidence per 100 000 population"]

    countries_to_keep = ["China",
        "Germany",
        "France",
        "Spain",
        "Italy",
        "Poland"]

    df = df[df['Country'].isin(countries_to_keep)]

    columns_to_keep = ["Variable", "Measure", "Country", "Year", "Value"] 
    df = df[columns_to_keep]
    
    pivoted_data_new = df.pivot_table(index=['Country', 'Variable'], columns='Year', values='Value')
    
    pivoted_data_new.reset_index(inplace=True)
    
    eu_countries_new = ['France', 'Germany', 'Poland', 'Italy', 'Spain']
    
    eu_data_new = pivoted_data_new[pivoted_data_new['Country'].isin(eu_countries_new)]
    
    eu_mean_new = eu_data_new.groupby('Variable').mean()
    
    eu_mean_new['Country'] = 'EU'
    
    eu_mean_new.reset_index(inplace=True)
    eu_mean_new = eu_mean_new[['Country', 'Variable'] + [col for col in eu_mean_new.columns if col not in ['Country', 'Variable']]]
    
    pivoted_data_with_eu_new = pd.concat([pivoted_data_new, eu_mean_new], ignore_index=True)
    
    pivoted_data_with_eu_new = pivoted_data_with_eu_new.rename(columns={'Variable': 'Indicator'})
    
    return pivoted_data_with_eu_new


######################################################

def file_exists(filename):
    return os.path.exists(os.path.join(PATH, filename))

def fetch_and_organize_pollution_data(api_url):
    # Check if the local file exists
    if file_exists(pollution_data_filename) and not fetch_from_web:
        # If file exists and fetch_from_web is False, load data from the file
        return pd.read_csv(os.path.join(PATH, pollution_data_filename))

    # Fetch data from the web --- cite: ChatGPT to make function and syntax
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")


    pollution_data = response.json()          

    dimensions = pollution_data['structure']['dimensions']['series']
    countries = {v['id']: v['name'] for dim in dimensions if dim['id'] == 'COU' for v in dim['values']}
    pollutants = {v['id']: v['name'] for dim in dimensions if dim['id'] == 'POL' for v in dim['values']}
    variables = {v['id']: v['name'] for dim in dimensions if dim['id'] == 'VAR' for v in dim['values']}

    years = pollution_data['structure']['dimensions']['observation'][0]['values']
    year_range = [int(year['id']) for year in years]

    air_pollution = pd.DataFrame(index=pd.MultiIndex.from_product([countries.values(), pollutants.values(), variables.values()]), columns=year_range)

    for series_key, series_data in pollution_data['dataSets'][0]['series'].items():
        indices = list(map(int, series_key.split(':')))
        country = countries[dimensions[0]['values'][indices[0]]['id']]
        pollutant = pollutants[dimensions[1]['values'][indices[1]]['id']]
        variable = variables[dimensions[2]['values'][indices[2]]['id']]

        for year_index_str, observation in series_data['observations'].items():
            year_index = int(year_index_str)
            year = year_range[year_index]
            air_pollution.at[(country, pollutant, variable), year] = observation[0]
            
    air_pollution.reset_index(inplace=True)

    air_pollution.columns = ['Country', 'Pollutant', 'Indicator'] + list(range(1990, 2022))
    
    # After processing, save the data to a local file for future use
    air_pollution.to_csv(os.path.join(PATH, pollution_data_filename), index=False)

    return air_pollution

    return air_pollution




def eu_air_pollution(df):
    
    countries = ['Germany', 'France', 'Spain', 'Italy', 'Poland']

    df_filtered = df[df['Country'].isin(countries)]

    df_eu = df_filtered.groupby(['Pollutant', 'Indicator']).mean().reset_index()

    df_eu['Country'] = 'EU'

    df_with_eu = pd.concat([df, df_eu], ignore_index=True)
    
    df_with_eu = df_with_eu.drop(columns=['Indicator'])
    df_with_eu = df_with_eu.rename(columns={'Pollutant': 'Indicator'})
    
    year_columns = df_with_eu.columns[2:]  # Assuming the first two columns are 'Country' and 'Indicator'
    df_with_eu[year_columns] = df_with_eu[year_columns].apply(pd.to_numeric, errors='coerce')

    return df_with_eu



######################################################

pollution_data = fetch_and_organize_pollution_data(pollution_data_url)

# Load and clean data using your functions
dataframes = {
    'china_mean_lst': load_fname(PATH, file_names[0]),
    'europe_mean_lst': load_fname2(PATH, file_names[1]),
    'climate_disasters_frequency': clean_fname3(load_fname3(PATH, file_names[2])),
    'CO2_emissions': clean_fname4(load_fname4(PATH, file_names[3])),
    'protection_exp': clean_fname5(load_fname5(PATH, file_names[4])),
    'env_taxes': clean_fname6(load_fname6(PATH, file_names[5])),
    'resp': load_fname7(PATH, file_names[6]),
    'health_exp': load_fname8(PATH, file_names[7]),
    'com_disease': load_fname9(PATH, file_names[8]),
    'air_pol': eu_air_pollution(fetch_and_organize_pollution_data(pollution_data_url))
}

# Save each dataframe to a CSV file
for name, df in dataframes.items():
    output_file_path = f'/Users/sandhyagarimella/Documents/GitHub/final-project-climate-and-health/Data/{name}.csv'
    df.to_csv(output_file_path, index=False)