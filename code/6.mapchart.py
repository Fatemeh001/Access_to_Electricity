import pandas as pd
import lightningchart as lc
import time
import numpy as np

# Load data
electricity_data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')

# License key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
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
electricity_data['ISO_A3'] = electricity_data['Code']  

# Filter data for the years 1990 to 2021 and only rows with valid ISO_A3 codes
electricity_data = electricity_data[(electricity_data['Year'] >= 1990) & (electricity_data['Year'] <= 2021)]
electricity_data = electricity_data.dropna(subset=['ISO_A3', 'Access to electricity (% of population)'])

# Prepare pivot table
pivot_data = electricity_data.pivot_table(index='Year', columns='ISO_A3', values='Access to electricity (% of population)', aggfunc='mean', fill_value=0)

# Setup dashboard with 2 rows and 2 columns
dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=2)

# Map chart (row 0, spans both columns)
map_chart = dashboard.MapChart(row_index=0, column_index=0, column_span=2)
map_chart.set_title("Global Electricity Access")

# Line chart for average electricity access across continents (row 1, column 0)
line_chart = dashboard.ChartXY(row_index=1, column_index=0)
line_chart.set_title("Average Electricity Access Over Time by Continent")


# Gauge chart to show global average (row 1, column 1)
gauge_chart = dashboard.GaugeChart(row_index=1, column_index=1)
gauge_chart.set_title("Global Average Electricity Access")
gauge_chart.set_angle_interval(start=225, end=-45)
gauge_chart.set_interval(start=0, end=100)
color=gauge_chart.set_value_indicators([
    {'start': 0, 'end': 25, 'color': lc.Color('red')},
    {'start': 25, 'end': 50, 'color': lc.Color('orange')},
    {'start': 50, 'end': 75, 'color': lc.Color('yellow')},
    {'start': 75, 'end': 100, 'color': lc.Color('green')},
])
gauge_chart.set_bar_thickness(30)
gauge_chart.set_value_indicator_thickness(10)




# Create a dictionary to store series for each continent
continent_series = {
    'Africa': line_chart.add_line_series().set_name("Africa"),
    'Asia': line_chart.add_line_series().set_name("Asia"),
    'Europe': line_chart.add_line_series().set_name("Europe"),
    'North America': line_chart.add_line_series().set_name("North America"),
    'South America': line_chart.add_line_series().set_name("South America"),
    'Oceania': line_chart.add_line_series().set_name("Oceania")
}

# Add a legend to the line chart
legend = line_chart.add_legend(horizontal=False, title="Continents")

# Attach each series to the legend
for series in continent_series.values():
    legend.add(series)




# Function to update map chart for a given year
def update_map_for_year(year, data):
    map_chart.invalidate_region_values([{"ISO_A3": item["category"], "value": item["value"]} for item in data])
    map_chart.set_title(f'Electricity Access by Country - Year {year}')
    
    # Update the map's color palette (0-100%)
    map_chart.set_palette_coloring(
        steps=[
            {'value': 0, 'color': lc.Color(0, 0, 255)},     
            {'value': 20, 'color': lc.Color(0, 128, 255)},
            {'value': 40, 'color': lc.Color(0, 255, 255)},  
            {'value': 60, 'color': lc.Color(0, 255, 128)},   
            {'value': 80, 'color': lc.Color(255, 255, 0)},    
            {'value': 90, 'color': lc.Color(255, 165, 0)},    
            {'value': 100, 'color': lc.Color(0, 255, 0)},    
        ],
        look_up_property='value'
   
    )

# Function to prepare data for each year
def prepare_data_for_year(year):
    year_data = pivot_data.loc[year].dropna()
    prepared_data = [{"category": country, "value": year_data[country]} for country in year_data.index]
    return prepared_data

# Function to calculate the average access for each continent
def calculate_continent_average(year):
    averages = {}
    for continent, countries in continent_map.items():
        continent_data = pivot_data.loc[year, pivot_data.columns.isin(countries)].dropna()
        if len(continent_data) > 0:
            averages[continent] = continent_data.mean()
        else:
            averages[continent] = 0
    return averages

# Function to calculate global average access for the gauge chart
def calculate_global_average(year):
    global_data = pivot_data.loc[year].dropna()
    return global_data.mean() if len(global_data) > 0 else 0


# Function to update the dashboard
def update_dashboard():
    # Lists to store data for each continent
    continent_data = {continent: [] for continent in continent_map.keys()}
    years = []

    for year in pivot_data.index:
        print(f"Updating data for year: {year}")
        data = prepare_data_for_year(year)

        # Update map chart for the current year
        update_map_for_year(year, data)

        # Calculate continent averages for the current year
        averages = calculate_continent_average(year)
        years.append(year)

        # Update each continent's series incrementally
        for continent, avg in averages.items():
            continent_data[continent].append(avg)
            continent_series[continent].add(year, avg)

        # Calculate and update the global average for the gauge chart
        global_avg = calculate_global_average(year)
        gauge_chart.set_value(global_avg)  # Update the gauge chart with global average
        gauge_chart.set_title(f"Global Average Electricity Access - Year {year}")


        # Delay for smoother visualization
        time.sleep(1)


dashboard.open(live=True)
update_dashboard()
