import pandas as pd
import lightningchart as lc
import time
import numpy as np
from sklearn.linear_model import LinearRegression



# Load the dataset
data = pd.read_csv('dataset/share-of-the-population-with-access-to-electricity.csv')
import lightningchart as lc
with open('A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


df_cleaned = data.drop(columns=['Code'])

countries = ['Afghanistan',  'Argentina', 'Brazil', 'India', 'Rwanda', 'United States']

country_trend = df_cleaned[df_cleaned['Entity'].isin(countries)]

pivot_data = country_trend.pivot(index='Year', columns='Entity', values='Access to electricity (% of population)')

pivot_data.index = pivot_data.index.map(int)

start_years = {country: pivot_data[country].first_valid_index() for country in countries}

# Create the line chart
chart = lc.ChartXY(title='Access to Electricity Over Time')

legend = chart.add_legend().set_position(x=15, y=30)

# Create series for each country
line_series = {}
prediction_series = {}  

for country in countries:
    # Create normal line series for the real data
    line_series[country] = chart.add_line_series().set_name(country)
    line_series[country].set_line_thickness(2)  
    legend.add(line_series[country])
    
    # Create dashed line series for predictions without adding them to the legend
    prediction_series[country] = chart.add_line_series().set_name(f'{country} (Prediction)')
    prediction_series[country].set_line_thickness(2).set_dashed('Dashed').set_line_color(lc.Color(255, 0, 0)) 

# Add a single prediction legend entry
legend.add(chart.add_line_series().set_name("Prediction (All)").set_line_color(lc.Color(255, 32, 0)).set_dashed('Dashed'))

# Set titles for the axes
chart.get_default_x_axis().set_title('Year')
chart.get_default_y_axis().set_title('Access to Electricity (%)')

# Extend the X axis to cover 10 years of predictions
chart.get_default_x_axis().set_tick_strategy('Numeric').set_interval(
    start=int(pivot_data.index.min()), 
    end=int(pivot_data.index.max() + 10)  
)

# Set the Y axis to be limited to 100 (since access cannot exceed 100%)
chart.get_default_y_axis().set_interval(0, 20)

# Open the chart for live updates
chart.open(live=True)

# Define a function to interpolate values between two points
def interpolate_points(x1, x2, y1, y2, steps=5): 
    x_values = np.linspace(x1, x2, steps)
    y_values = np.linspace(y1, y2, steps)
    return x_values, y_values

# Prepare interpolated data for all countries and years (including future predictions)
interpolated_data = {country: [] for country in countries}
future_predictions_data = {country: [] for country in countries} 

# Linear regression for each country to predict the next 10 years
for country in countries:
    country_data = pivot_data[country].dropna()
    
    if len(country_data) > 1:  # Ensure there's enough data for regression
        X = np.array(country_data.index).reshape(-1, 1)
        y = np.array(country_data.values)  
        
        # Fit the linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        future_years = np.array([pivot_data.index.max() + i for i in range(1, 11)]).reshape(-1, 1)
        future_predictions = model.predict(future_years)
        
        # Limit predictions to 100% (since it cannot exceed 100%)
        future_predictions = np.clip(future_predictions, 0, 100)

        # Add real data to interpolated_data
        for year_idx in range(len(country_data.index) - 1):
            current_year = country_data.index[year_idx]
            next_year = country_data.index[year_idx + 1]
            
            if current_year >= start_years[country]:
                if not pd.isna(pivot_data.loc[current_year, country]) and not pd.isna(pivot_data.loc[next_year, country]):
                    # Interpolate between current year and next year for smoother transition
                    x_interp, y_interp = interpolate_points(current_year, next_year, 
                                                            pivot_data.loc[current_year, country], 
                                                            pivot_data.loc[next_year, country], steps=30)  
                    for i in range(len(x_interp)):
                        interpolated_data[country].append((float(x_interp[i]), float(y_interp[i])))

        # Add future predictions to future_predictions_data
        last_real_year = country_data.index[-1]
        last_real_value = country_data.values[-1]
        future_predictions_data[country].append((float(last_real_year), float(last_real_value)))

        for i in range(len(future_years)):
            future_predictions_data[country].append((float(future_years[i]), float(future_predictions[i])))

# Add interpolated points for all countries, respecting their start year
max_steps = max([len(data) for data in interpolated_data.values()])
for i in range(max_steps):
    for country in countries:
        if i < len(interpolated_data[country]):
            x_val, y_val = interpolated_data[country][i]
            if x_val >= start_years[country]:  
                line_series[country].add(x_val, y_val)


# Add predicted data as dashed lines (for the next 10 years)
max_pred_steps = max([len(data) for data in future_predictions_data.values()])
for i in range(max_pred_steps):
    for country in countries:
        if i < len(future_predictions_data[country]):
            x_val, y_val = future_predictions_data[country][i]
            if x_val >= start_years[country]: 
                prediction_series[country].add(x_val, y_val)

    time.sleep(0.1)  

