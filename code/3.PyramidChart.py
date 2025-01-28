import pandas as pd
import lightningchart as lc
import numpy as np

# Load data
data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')

# License key
with open('A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Add a dictionary mapping countries to their respective continents
continent_map = {
    'Africa': ['AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'CIV', 'COD', 'DJI', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MYT', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TGO', 'TZA', 'UGA', 'ZMB', 'ZWE'],
    'Asia': ['AFG', 'BGD', 'BTN', 'KHM', 'CHN', 'IND', 'IDN', 'IRN', 'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'KWT', 'KGZ', 'LAO', 'LBN', 'MDV', 'MNG', 'MMR', 'NPL', 'OMN', 'PAK', 'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'KOR', 'LKA', 'SYR', 'TJK', 'THA', 'TLS', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM'],
    'Europe': ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR', 'UKR', 'GBR'],
    'North America': ['BLZ', 'CAN', 'CRI', 'CUB', 'DOM', 'SLV', 'GTM', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'USA'],
    'South America': ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN'],
    'Oceania': ['AUS', 'FJI', 'KIR', 'MHL', 'FSM', 'NRU', 'NZL', 'PLW', 'PNG', 'WSM', 'SLB', 'TON', 'TUV', 'VUT']
}

# Ensure ISO_A3 codes are correct (in your data you already have 'KAZ' for Kazakhstan)
data['ISO_A3'] = data['Code']  

# Filter data for the year 2021 and only rows with valid ISO_A3 codes
electricity_data = data[data['Year'] == 2021]
electricity_data = electricity_data.dropna(subset=['ISO_A3', 'Access to electricity (% of population)'])

# Prepare pivot table
pivot_data = electricity_data.pivot_table(index='Year', columns='ISO_A3', values='Access to electricity (% of population)', aggfunc='mean', fill_value=0)

# Calculate the average access for each continent
def calculate_continent_average():
    averages = {}
    for continent, countries in continent_map.items():
        continent_data = pivot_data.loc[2021, pivot_data.columns.isin(countries)].dropna()
        if len(continent_data) > 0:
            averages[continent] = continent_data.mean()
        else:
            averages[continent] = 0
    return averages

# Get continent averages
continent_averages = calculate_continent_average()

# Prepare data for PyramidChart (sorted by value in descending order)
data = [{"name": continent, "value": round(average, 2)} for continent, average in continent_averages.items()]
sorted_data = sorted(data, key=lambda x: x["value"], reverse=False) 

# Create PyramidChart
chart = lc.PyramidChart(
    slice_mode='height',
    theme=lc.Themes.Dark,
    title='Electricity Access Pyramid by Continent (2021)'
)

# Add data to the PyramidChart
chart.add_slices(sorted_data)

# Add legend to the PyramidChart
chart.add_legend().add(chart).set_title('Electricity Access Pyramid')

# Open the chart
chart.open()



