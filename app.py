import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px
import pandas as pd

# Sample data
def load_data():
    data = pd.read_csv('assets/healthcare.csv')
    data['Billing Amount'] = pd.to_numeric(data['Billing Amount'], errors = 'coerce')
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')
    data['YearMonth'] = data['Date of Admission'].dt.to_period('M')
    print("Data loaded successfully")
    print(f"Dataset shape: {data.shape}")
    return data

data = load_data()

num_patients = len(data['Name'].unique())
avg_billing_amount = data['Billing Amount'].mean()

# Create a Dahs Application
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([

    # Text Header
    dbc.Row([
        dbc.Col(
            html.H1("Healthcare Billing Dashboard", className="text-center"),
            width=12
        )
    ], className="mb-4"), 

    # Summary Statistics
    dbc.Row([
        dbc.Col(
            html.H2(f"Total Patients: {num_patients}", className="text-center"),
            width=6
        ),

        dbc.Col(
            html.H2(f"Average Billing Amount: ${avg_billing_amount:.0f}", className = "text-center"),
            width=6
        )
    ], className="mb-4"),

    # Cards for Demographics, Medical Conditions, Insurance Providers, Billing Amounts, and Trends
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Patient Demographic", className="card-title"),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[{"label": gender, "value": gender} for gender in data["Gender"].unique()],
                        value=None,
                        placeholder="Select a gender"
                    )
                ])
            ])
        ], width=6),
   
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Medical Condition Distribution", className="card-title"),
                    dcc.Graph(id="age-distribution")
                ])
            ])
        ], width=6)

    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Insurance Provider Comparison", className="card=title"),
                    dcc.Graph(id="insurance-comparison"),
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Billin Amount Distribution", className="card-title"),
                    dcc.Slider(
                        id='billing-slider',
                        min = data['Billing Amount'].min(),
                        max = data['Billing Amount'].max(),
                        value = data['Billing Amount'].mean(),
                        marks = {int(value): f"${int(value):,}" for value in data['Billing Amount'].quantile([0, 0.25, 0.5, 0.75, 1]).values},
                        step=10
                    ),
                    dcc.Graph(id="billing-distribution")
                ])
            ])
        ])
    ], className="mb-4"),

    # Trends in admission Over Time
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Trends in Admission Over Time", className="card-title"),
                    dcc.Graph(id="admission-trends"),
                    dcc.RadioItems(
                        id="chart-type",
                        options =[
                            {"label":"Line Chart","value": "line"},
                            {"label":"Bar Chart", "value": "bar"}
                        ],
                        value="line",
                        inline=True,
                        className="mb-4"
                    ),

                    dcc.Dropdown(
                        id="condition-filter",
                        options=[{"label": condition, "value": condition} for condition in data["Medical Condition"].unique()]
                    )
                ])
            ])
        ])
    ])

], fluid=True)

# Prepare Callbacks
@app.callback(
    Output('age-distribution', 'figure'),
    Input('gender-filter', 'value')
)
def update_distribution(selected_gender):
    if selected_gender:
        filtered_df = data[data["Gender"]== selected_gender]
    else:
        filtered_df = data

    if filtered_df.empty:
        return {}
    
    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=10,
        color="Gender",
        title="Age Distribution by Gender",
        color_discrete_sequence=["blue", "pink"]
    )
    
    return fig


if __name__ =='__main__':
    app.run(debug=True)