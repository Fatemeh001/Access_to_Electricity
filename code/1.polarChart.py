
import pandas as pd
import lightningchart as lc
import time
import numpy as np
import random

# Load data
data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')

# License key
with open('A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Function to filter and prepare data for a given country
def get_country_data(country_name):
    country_data = data[data['Entity'] == country_name]
    return country_data['Year'].values, country_data['Access to electricity (% of population)'].values

# Initialize the chart in real-time mode
chart = lc.PolarChart(theme=lc.Themes.TurquoiseHexagon, title="Access to Electricity in Polar Chart").open(live=True)

# Function to generate random color
def get_random_color():
    return lc.Color(f'#{random.randint(0, 0xFFFFFF):06x}')

# List of selected countries
selected_countries = ['Guinea-Bissau', 'Rwanda', 'Zambia', 'Nigeria', 'Sudan', 'Panama', 
                      'Somalia', 'Lesotho', 'Liberia', 'South Sudan', 'Afghanistan', 'Botswana', 
                      'Kenya', 'Nepal']

# Create a dictionary to store line series for each country
country_series = {}

# Initialize line series for each country with empty data
for index, country in enumerate(selected_countries):
    color = get_random_color()
    line_series = chart.add_point_line_series().set_name(country)  # Set the name of the series to the country name
    line_series.set_stroke(thickness=2, color=color)
    
    # Set highlight for specific series (e.g., alternating highlight)
    if index % 2 == 0:
        line_series.set_highlight(1)  
    else:
        line_series.set_highlight(0.5)  
    
    country_series[country] = line_series

# Adding a legend to the chart
legend = lc.ui.legend.Legend(chart, horizontal=False, title="Country Legend")

for country in selected_countries:
    legend.add(country_series[country])

legend.set_font_size(14).set_padding(10)

def update_data():
    steps_per_year = 10

    min_year = min([get_country_data(country)[0][0] for country in selected_countries])
    max_year = max([get_country_data(country)[0][-1] for country in selected_countries])

    total_years = max_year - min_year + 1

    # Create a dictionary to store all points for each country
    for country in selected_countries:
        country_series[country].all_data_points = []

    # Iterate over all possible years (from min_year to max_year)
    for year in range(min_year, max_year):
        for step in range(steps_per_year):
            for country in selected_countries:
                try:
                    # Get data for each country
                    years, access_data = get_country_data(country)

                    # If the country doesn't have data for the current year, skip it
                    if year < years[0] or year > years[-1]:
                        continue

                    year_index = np.where(years == year)[0][0]
                    
                    if year_index < len(years) - 1:
                        current_year = years[year_index]
                        next_year = years[year_index + 1]
                        current_access = access_data[year_index]
                        next_access = access_data[year_index + 1]

                        interp_year = np.interp(step, [0, steps_per_year], [current_year, next_year])
                        interp_access = np.interp(step, [0, steps_per_year], [current_access, next_access])
                    else:
                        interp_year = years[year_index]
                        interp_access = access_data[year_index]

                    angle = np.interp(interp_year, (min_year, max_year), (0, 360))

                    country_series[country].all_data_points.append({'angle': angle, 'amplitude': interp_access})

                    # Update the series for the country
                    country_series[country].set_data(country_series[country].all_data_points)

                except Exception as e:
                    print(f"Error updating data for {country}: {e}")

        time.sleep(0.001)
x = chart.get_radial_axis()
x.set_division(27)
x.set_tick_labels([
'1990',
'1991',
'1992',
'1993',
'1994',
'1995',
'1996',
'1997',
'1998',
'1999',
'2000',
'2001',
'2002',
'2003',
'2004',
'2005',
'2006',
'2007',
'2008',
'2009',
'2010',
'2011',
'2012',
'2013',
'2014',
'2015',
'2016',
'2017',
'2018',
'2019',
'2020',
'2021',
])

update_data()

