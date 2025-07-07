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
                        id="demographic-dropdown",
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
                        max = data['Billing Amount'].max()
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
                    dcc.RadioItems(id="chart-type")
                ])
            ])
        ], width=12)
    ])

])

if __name__ =='__main__':
    app.run(debug=True)