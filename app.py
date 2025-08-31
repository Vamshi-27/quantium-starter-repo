import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load and prepare data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(style={
    "fontFamily": "Segoe UI, sans-serif",
    "backgroundColor": "#0d1117",  # GitHub dark
    "backgroundImage": "radial-gradient(ellipse at top, #1a1f2c 0%, transparent 70%), "
                       "radial-gradient(ellipse at bottom, #0b0f17 0%, transparent 80%)",
    "minHeight": "100vh",
    "padding": "30px",
    "color": "white"
}, children=[
    # Header
    html.H1("✨ Pink Morsel Sales Dashboard", 
        style={
            "textAlign": "center",
            "color": "#e6edf3",
            "marginBottom": "30px",
            "fontSize": "40px",
            "fontWeight": "700",
            "textShadow": "0 0 12px rgba(255,255,255,0.3)"
        }
    ),

    # KPI cards
    html.Div(style={
        "display": "flex", 
        "gap": "20px", 
        "justifyContent": "center", 
        "margin": "20px 0"
    }, children=[
        html.Div([
            html.H4("💰 Total Sales", style={"margin": "0", "color": "#9baec8"}),
            html.H2(f"${df['Sales'].sum():,.0f}", style={"margin": "0", "color": "#f0f6fc"})
        ], style={
            "flex": 1, 
            "background": "#161b22", 
            "padding": "20px", 
            "borderRadius": "16px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.6)", 
            "textAlign": "center"
        }),

        html.Div([
            html.H4("📊 Avg Daily Sales", style={"margin": "0", "color": "#9baec8"}),
            html.H2(f"${df['Sales'].mean():,.0f}", style={"margin": "0", "color": "#f0f6fc"})
        ], style={
            "flex": 1, 
            "background": "#161b22", 
            "padding": "20px", 
            "borderRadius": "16px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.6)", 
            "textAlign": "center"
        }),

        html.Div([
            html.H4("🚀 Peak Sales", style={"margin": "0", "color": "#9baec8"}),
            html.H2(f"${df['Sales'].max():,.0f}", style={"margin": "0", "color": "#f0f6fc"})
        ], style={
            "flex": 1, 
            "background": "#161b22", 
            "padding": "20px", 
            "borderRadius": "16px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.6)", 
            "textAlign": "center"
        }),
    ]),

    # Region filter
    html.Div([
        html.Label("Select Region:", style={"fontWeight": "600", "fontSize": "18px", "color": "#f0f6fc"}),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "🌍 All", "value": "all"},
                {"label": "⬆️ North", "value": "north"},
                {"label": "➡️ East", "value": "east"},
                {"label": "⬇️ South", "value": "south"},
                {"label": "⬅️ West", "value": "west"}
            ],
            value="all",
            inline=True,
            style={"marginTop": "10px", "color": "#9baec8"}
        )
    ], style={
        "margin": "20px auto", 
        "background": "#161b22", 
        "padding": "20px",
        "borderRadius": "16px",
        "boxShadow": "0 4px 15px rgba(0,0,0,0.6)", 
        "width": "70%",
        "textAlign": "center"
    }),

    # Chart container
    html.Div([
        dcc.Graph(id="sales-chart", style={"height": "600px"})
    ], style={
        "background": "#161b22", 
        "padding": "20px",
        "borderRadius": "16px",
        "boxShadow": "0 4px 20px rgba(0,0,0,0.8)"
    })
])

# Callback for chart update
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    fig = go.Figure()

    if selected_region == "all":
        for region in df["Region"].unique():
            region_df = df[df["Region"] == region]
            fig.add_trace(go.Scatter(
                x=region_df["Date"], y=region_df["Sales"],
                mode="lines", name=region.title()
            ))
        title = "🌍 Sales Across All Regions"
    else:
        filtered_df = df[df["Region"] == selected_region]
        fig.add_trace(go.Scatter(
            x=filtered_df["Date"], y=filtered_df["Sales"],
            mode="lines+markers", name=selected_region.title(),
            line=dict(width=3, color="#58a6ff")
        ))
        title = f"📍 {selected_region.title()} Region Sales"

    # Add vertical line for price change
    fig.add_shape(
        type="line", x0="2021-01-15", x1="2021-01-15",
        y0=0, y1=1, yref="paper",
        line=dict(color="#ff4d4d", width=2, dash="dash")
    )
    fig.add_annotation(
        x="2021-01-15", y=1, yref="paper", showarrow=False,
        text="💰 Price Increase", bgcolor="#ff4d4d", font=dict(color="white")
    )

    fig.update_layout(
        title=title,
        xaxis_title="Date", yaxis_title="Sales ($)",
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#0d1117",
        font=dict(color="#c9d1d9")
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
