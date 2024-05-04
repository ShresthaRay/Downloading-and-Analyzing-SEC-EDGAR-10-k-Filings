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
        financials = yf.Ticker(input_data).financials.T  # Transpose the DataFrame
        
        # Check if 'Total Revenue' column is available
        if 'Total Revenue' in financials.columns:
            revenue = financials['Total Revenue']
            # Extract years from datetime indices
            x_axis_labels = [date for date in revenue.index]

            # Plot the Total Revenue data
            graph = dcc.Graph(
                id="revenue-graph",
                figure={
                    'data': [
                        {'x': x_axis_labels, 'y': revenue.values, 'type': 'line', 'name': 'Total Revenue'}
                    ],
                    'layout': {
                        'title': 'Total Revenue Trend',
                        'xaxis': {'title': 'Year'},  # Set x-axis title
                        'yaxis': {'title': 'Total Revenue ($)'}  # Set y-axis title
                    }
                }
            )
        else:
            graph = html.Div("Total Revenue data not available for this stock.")
 
    except Exception as e:
        error_message = f"Error retrieving financial data: {str(e)}"
        graph = html.Div(error_message)
 
    return graph

if __name__ == '__main__':
    app.run_server()