import pandas as pd
import lightningchart as lc

# Load data
data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')

# License key
with open('A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Define continent map
continent_map = {
    'Africa': ['AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'CIV', 'COD', 'DJI', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MYT', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TGO', 'TZA', 'UGA', 'ZMB', 'ZWE'],
    'Asia': ['AFG', 'BGD', 'BTN', 'KHM', 'CHN', 'IND', 'IDN', 'IRN', 'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'KWT', 'KGZ', 'LAO', 'LBN', 'MDV', 'MNG', 'MMR', 'NPL', 'OMN', 'PAK', 'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'KOR', 'LKA', 'SYR', 'TJK', 'THA', 'TLS', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM'],
    'Europe': ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR', 'UKR', 'GBR'],
    'North America': ['BLZ', 'CAN', 'CRI', 'CUB', 'DOM', 'SLV', 'GTM', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'USA'],
    'South America': ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN'],
    'Oceania': ['AUS', 'FJI', 'KIR', 'MHL', 'FSM', 'NRU', 'NZL', 'PLW', 'PNG', 'WSM', 'SLB', 'TON', 'TUV', 'VUT']
}

# Add ISO_A3 codes to the data
data['ISO_A3'] = data['Code']

# Filter data for each decade
decades = [1990, 2000, 2010, 2020]  # Ordered from least to greatest
filtered_data = data[data['Year'].isin(decades)]

# Prepare pivot table
pivot_data = filtered_data.pivot_table(index='Year', columns='ISO_A3', values='Access to electricity (% of population)', aggfunc='mean', fill_value=0)

# Calculate the average access for each continent in each decade
def calculate_decade_averages():
    decade_averages = []
    for year in sorted(decades):  
        averages = {}
        for continent, countries in continent_map.items():
            continent_data = pivot_data.loc[year, pivot_data.columns.isin(countries)].dropna()
            if len(continent_data) > 0:
                averages[continent] = continent_data.mean()
            else:
                averages[continent] = 0
        decade_averages.append(averages)
    return decade_averages

# Get the averages for each decade
decade_averages = calculate_decade_averages()

# Prepare data for Grouped Bar Chart
grouped_data = []
for continent in continent_map.keys():
    continent_values = [round(averages[continent], 2) for averages in decade_averages]
    grouped_data.append({'subCategory': continent, 'values': continent_values})

# Create the Grouped Bar Chart
chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.Light,
    title='Electricity Access by Decade and Continent'
)

# Set data for Grouped Bar Chart (decades as main categories)
chart.set_data_grouped(
    ['1990', '2000', '2010', '2020'],
    grouped_data
)

chart.add_legend().add(chart)

# Open the chart
chart.open()
