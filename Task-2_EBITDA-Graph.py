import datetime
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
app.title = "Financial Statements Visualization"
 
app.layout = html.Div(children=[
    html.H1("Financial Statements Dashboard"),
    html.H4("Please enter the stock ticker symbol"),
    dcc.Input(id='input', value='AAPL', type='text'),
    html.Div(id='output-graph')
])

# Callback decorator 
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    start = datetime.datetime(1995, 1, 1)
    end = datetime.datetime.now()
 
    try:
        # Fetch financial statements data
        financials = yf.Ticker(input_data).financials
        
        # Extract the Normalized EBITDA data using its index (assuming it's the first column)
        normalized_ebitda = financials.iloc[:, 0]
        # Extract years from datetime indices
        x_axis_labels = [date for date in range (1995,2024)]

        # Plot the normalized EBITDA data
        graph = dcc.Graph(
            id="ebitda-graph",
            figure={
                'data': [
                    {'x': x_axis_labels, 'y': normalized_ebitda.values, 'type': 'line', 'name': 'Normalized EBITDA'}
                ],
                'layout': {
                    'title': 'Normalized EBITDA Trend',
                    'xaxis': {'title': 'Year'},  # Set x-axis title
                    'yaxis': {'title': 'Normalized EBITDA'}  # Set y-axis title
                }
            }
        )
 
    except Exception as e:
        error_message = f"Error retrieving financial data: {str(e)}"
        graph = html.Div(error_message)
 
    return graph

if __name__ == '__main__':
    app.run_server()
