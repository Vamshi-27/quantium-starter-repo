import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import datetime

# Load the sales data
df = pd.read_csv("formatted_sales_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Create line chart: Sales over time
fig = px.line(df, x="Date", y="Sales", title="Pink Morsel Sales Over Time")

# Add vertical line for price increase (15 Jan 2021) using add_shape
fig.add_shape(
    type="line",
    x0="2021-01-15", x1="2021-01-15",
    y0=0, y1=1,
    yref="paper",
    line=dict(color="red", width=2, dash="dash"),
)

# Add annotation for the vertical line
fig.add_annotation(
    x="2021-01-15",
    y=0.95,
    yref="paper",
    text="Price Increase",
    showarrow=False,
    textangle=0,
    xanchor="left"
)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Visualizer", style={
        "textAlign": "center", 
        "fontFamily": "Times New Roman", 
        "color": "blue"
    }),  # Header
    dcc.Graph(id="sales-chart", figure=fig)  # Line chart
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
