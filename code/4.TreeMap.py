import pandas as pd
import lightningchart as lc

# Load data
electricity_data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')

# License key
with open('A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


# Mapping countries to continents
continent_map = {
    'Africa': ['AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'CIV', 'COD', 'DJI', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MYT', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TGO', 'TZA', 'UGA', 'ZMB', 'ZWE'],
    'Asia': ['AFG', 'BGD', 'BTN', 'KHM', 'CHN', 'IND', 'IDN', 'IRN', 'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'KWT', 'KGZ', 'LAO', 'LBN', 'MDV', 'MNG', 'MMR', 'NPL', 'OMN', 'PAK', 'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'KOR', 'LKA', 'SYR', 'TJK', 'THA', 'TLS', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM'],
    'Europe': ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR', 'UKR', 'GBR'],
    'North America': ['BLZ', 'CAN', 'CRI', 'CUB', 'DOM', 'SLV', 'GTM', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'USA'],
    'South America': ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN'],
    'Oceania': ['AUS', 'FJI', 'KIR', 'MHL', 'FSM', 'NRU', 'NZL', 'PLW', 'PNG', 'WSM', 'SLB', 'TON', 'TUV', 'VUT']
}

# Filter and clean data
electricity_data = electricity_data.dropna(subset=['Code', 'Access to electricity (% of population)'])

# Create TreeMap data structure
treemap_data = []
for continent, countries in continent_map.items():
    continent_node = {'name': continent, 'children': []}
    for country in countries:
        access_value = electricity_data.loc[electricity_data['Code'] == country, 'Access to electricity (% of population)'].mean()
        if pd.notna(access_value):
            continent_node['children'].append({'name': country, 'value': access_value})
    if continent_node['children']:
        treemap_data.append(continent_node)

# Create TreeMapChart
chart = lc.TreeMapChart(
    theme=lc.Themes.Dark,
    title="Electricity Access by Continent (2021)"
)

# Set data
chart.set_data(treemap_data)

# Customize appearance
color=chart.set_node_coloring(
    steps=[
        {'value': 0, 'color': lc.Color('red')},
        {'value': 50, 'color': lc.Color('yellow')},
        {'value': 100, 'color': lc.Color('green')}
    ]
)

# Add legend

legend = chart.add_legend()
legend.set_position(20, 20)  
legend.set_margin(10)
legend.add(color)

# Open chart
chart.open()


