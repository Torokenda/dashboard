import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import numpy as np

app = dash.Dash(__name__)

# Read energy consumption data
energy_data = pd.read_csv('energy_consumption_data.csv')
energy_data['date'] = pd.to_datetime(energy_data['date'])

# Read appliance power consumption data
appliance_data = pd.read_csv('appliance_power_consumption.csv')

# Calculate total energy consumption for the house
total_energy_consumption = appliance_data['power_consumption'].sum()

# Define the average power consumption per 5 seconds
average_power_consumption_per_5_seconds = 0.005

# Layout the dashboard
app.layout = html.Div([
    dcc.Interval(id='interval', interval=5000, n_intervals=0),  # Update every 5 seconds
    html.Div([
        html.Div(id='total-energy-consumption-display', style={'font-size': '36px', 'margin-top': '20px'}),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=energy_data['date'].min(),
            max_date_allowed=energy_data['date'].max(),
            start_date=energy_data['date'].min(),
            end_date=energy_data['date'].max()
        )
    ]),
    html.Div([
        dcc.Graph(id='energy-consumption-graph', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='energy-consumption-trend-graph', style={'display': 'inline-block', 'width': '50%'})
    ]),
    dcc.Graph(id='appliance-power-pie-chart')
])

# Update total energy consumption display every 5 seconds
@app.callback(
    Output('total-energy-consumption-display', 'children'),
    [Input('interval', 'n_intervals')]
)
def update_total_energy_consumption_display(n):
    # Simulate real-time data by generating a random value within the specified range
    random_increment = np.random.uniform(0.004, 0.006)
    global total_energy_consumption
    total_energy_consumption += random_increment
    total_cost = total_energy_consumption * 20  # Multiply kWh by price per kWh (20 shillings)
    return html.Div([
        html.Div(f"Total Energy Consumption: {total_energy_consumption:.2f} kWh"),
        html.Div(f"Total Cost: Ksh {total_cost:.2f}")
    ])

# Update energy consumption graph based on date range selection
@app.callback(
    Output('energy-consumption-graph', 'figure'),
    [Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_energy_consumption_graph(start_date, end_date):
    filtered_data = energy_data[(energy_data['date'] >= start_date) & (energy_data['date'] <= end_date)]

    figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data['date'],
                y=filtered_data['energy_consumption'],
                name='Energy Consumption',
                mode='lines'
            )
        ],
        layout={
            'title': 'Energy Consumption',
            'xaxis': {
                'title': 'Date'
            },
            'yaxis': {
                'title': 'Energy Consumption (kWh)'
            }
        }
    )

    return figure

# Update energy consumption trend graph based on date range selection
@app.callback(
    Output('energy-consumption-trend-graph', 'figure'),
    [Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_energy_consumption_trend_graph(start_date, end_date):
    filtered_data = energy_data[(energy_data['date'] >= start_date) & (energy_data['date'] <= end_date)]

    figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data['date'],
                y=filtered_data['energy_consumption'].rolling(window=7).mean(),
                name='Energy Consumption Trend',
                mode='lines'
            )
        ],
        layout={
            'title': 'Energy Consumption Trend',
            'xaxis': {
                'title': 'Date'
            },
            'yaxis': {
                'title': 'Energy Consumption (kWh)'
            }
        }
    )

    return figure

@app.callback(
    Output('appliance-power-pie-chart', 'figure'),
    [Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_appliance_power_pie_chart(start_date, end_date):
    # Calculate total power consumption for each appliance
    appliance_grouped = appliance_data.groupby('appliance')['power_consumption'].sum().reset_index()

    figure = go.Figure(
        data=[go.Pie(labels=appliance_grouped['appliance'],
                     values=appliance_grouped['power_consumption'],
                     hole=0.3)],
        layout={'title': 'Total Appliance Power Consumption'}
    )

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
