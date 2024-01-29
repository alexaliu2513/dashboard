import dash
from dash import dcc, html
import pandas as pd
pd.set_option('display.max_rows', 20)
import numpy as np

import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

from dash.dependencies import Input, Output
from datetime import date
from datetime import datetime
import dash_bootstrap_components as dbc

from googletrans import Translator
translator = Translator()

import calendar


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app.title = 'E-commerce Order Dashboard'

merge = pd.read_csv('Orders_merged.csv')

customer_states = merge['customer_state'].unique()

card_content_a = [
    dbc.CardHeader(
        [
            html.Div([html.I(className="bi bi-basket"), "Total Number of Orders"], className="text-center"),
        ]
    ),
    dbc.CardBody(
        [
            html.H1(id="num-a", className="text-center"),
        ],
    ),
]
card_content_b = [
    dbc.CardBody(
        [
            html.H1(id="num-b", className="text-center"),
        ],
    ),
    dbc.CardFooter(
        [
            html.Div([html.I(className="bi bi-hand-thumbs-up"), "Average Review Score"], className="text-center"),
        ]
    ),
]
card_content_c = [
    dbc.CardHeader(
        [
            html.Div([html.I(className="bi bi-phone-vibrate"), "Average Response Time"], className="text-center"),
        ]
    ),
    dbc.CardBody(
        [
            html.Div([
                html.H1(id="num-c"),
                dbc.Badge(
                            "mins",
                            color="white",
                            text_color="primary",
                            className="border me-1",
                ),
            ], className="text-center", style={"display": "flex", "justify-content": "center", "align-items": "center"}),
        ],
    ),
]
card_content_d = [
    dbc.CardBody(
        [
            html.Div([
                html.H1(id="num-d"),
                dbc.Badge("days", color="primary", className="me-1"),
            ], className="text-center",
                style={"display": "flex", "justify-content": "center", "align-items": "center"}),
        ],
    ),
    dbc.CardFooter(
        [
            html.Div([html.I(className="bi bi-box-seam"), "Average Delivery Time"], className="text-center"),
        ]
    ),
]
card_content_f = [
    dbc.CardBody(
        [
            html.Div([
                html.H1(id="num-f"),
                dbc.Badge("T R $", color="primary", className="me-1"),
            ], className="text-center",
                style={"display": "flex", "justify-content": "center", "align-items": "center"}),
        ],
    ),
    dbc.CardFooter(
        [
            html.Div([html.I(className="bi bi-journal-check"), "Total Transaction Value"], className="text-center"),
        ]
    ),
]
card_content_e = [
    dbc.CardHeader(
        [
            html.Div([html.I(className="bi bi-currency-dollar"), "Average Transaction Value"], className="text-center"),
        ]
    ),
    dbc.CardBody(
        [
            html.Div([
                html.H1(id="num-e"),
                dbc.Badge(
                    "R $",
                    color="white",
                    text_color="primary",
                    className="border me-1",
                ),
            ], className="text-center",
                style={"display": "flex", "justify-content": "center", "align-items": "center"}),
        ],
    ),
]
card_content_h = [
    dbc.CardBody(
        [
            html.H1(id="num-h", className="text-center"),
        ],
    ),
    dbc.CardFooter(
        [
            html.Div([html.I(className="bi bi-person"), "Total Number of Customers"], className="text-center"),
        ]
    ),
]
card_content_g = [
    dbc.CardHeader(
        [
            html.Div([html.I(className="bi bi-shop"), "Total Number of Sellers"], className="text-center"),
        ]
    ),
    dbc.CardBody(
        [
            html.H1(id="num-g", className="text-center"),
        ],
    ),
]

app.layout = dbc.Container(
    [
        html.H1("E-commerce Order Dashboard", className="text-center"),

        dbc.Row(
            [
                dbc.Col(
                    dcc.DatePickerRange(
                            id='date-picker-range',
                            min_date_allowed=date(2016, 10, 3),
                            max_date_allowed=date(2018, 8, 29),
                            start_date='2016-10-03',
                            end_date='2018-08-29',
                            display_format='YYYY-MM-DD'
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                            id='state-dropdown',
                            options=[{'label': state, 'value': state} for state in customer_states],
                            multi=True,
                            placeholder='Select State(s)'
                    ),
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content_a, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content_b, color="primary", outline=True)),
                dbc.Col(dbc.Card(card_content_c, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content_d, color="primary", outline=True)),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content_f, color="primary", outline=True)),
                dbc.Col(dbc.Card(card_content_e, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content_h, color="primary", outline=True)),
                dbc.Col(dbc.Card(card_content_g, color="primary", inverse=True)),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='bar-chart-b'
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id='pie-chart',
                        figure=px.pie(merge, names='payment_type', values='payment_value',title='Payment Type Distribution', color='payment_type',color_discrete_sequence=px.colors.sequential.Blues)
                    ),
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='scatter-plot',
                        figure=px.scatter(merge, x='order_purchase_timestamp', y='payment_value', color='order_status', title='Purchase Amount Over Time')
                    ),
                ),
                dbc.Col(
                    dcc.Graph(
                        id='bar-chart-a',
                        figure=px.bar(merge, x='review_score', title='Review Score Amount Over Time')
                    ),
                )
            ]
        ),
        dcc.Graph(
            id='heat-map'
        ),
    ]
)

@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bar-chart-a', 'figure'),
     Output('bar-chart-b', 'figure'),
     Output('heat-map', 'figure'),
     Output('num-a', 'children'),
     Output('num-b', 'children'),
     Output('num-c', 'children'),
     Output('num-d', 'children'),
     Output('num-f', 'children'),
     Output('num-e', 'children'),
     Output('num-h', 'children'),
     Output('num-g', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('state-dropdown', 'value')]
)
def update_plots(start_date, end_date, selected_states):
    # If no state is selected, consider all states
    if selected_states is None or not selected_states:
        selected_states = merge['customer_state'].unique()

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    merge['order_purchase_timestamp'] = pd.to_datetime(merge['order_purchase_timestamp'])

    filtered_df = merge[(merge['order_purchase_timestamp'] >= start_date) &
                        (merge['order_purchase_timestamp'] <= end_date) &
                        (merge['customer_state'].isin(selected_states))]

    filtered_df['Weekday'] = filtered_df['order_purchase_timestamp'].dt.dayofweek
    filtered_df['Week_Number'] = np.ceil((filtered_df['order_purchase_timestamp'] - start_date).dt.days / 7).astype(int) + 1
    filtered_df['order_delivered_customer_date'] = pd.to_datetime(filtered_df['order_delivered_customer_date'])
    filtered_df['order_status'] = np.where(filtered_df['order_delivered_customer_date'] > end_date, 'not delivered', 'delivered')

    scatter_fig = px.scatter(filtered_df, x='order_purchase_timestamp', y='payment_value', color='order_status', title='Purchase Amount Over Time')
    scatter_fig.update_layout(xaxis_title='Time', yaxis_title='Payment Value', legend_title_text='Order Status')

    pie_fig = px.pie(filtered_df, names='payment_type', values='payment_value', title='Payment Type Distribution', color='payment_type', color_discrete_sequence=px.colors.sequential.Blues)

    df_frequency = filtered_df['review_score'].value_counts().reset_index()
    df_frequency.columns = ['review_score', 'frequency']
    bar_fig_a = px.bar(df_frequency, x='review_score', y='frequency', title='Review Score Amount Over Time')
    bar_fig_a.update_layout(xaxis_title='Review Score', yaxis_title='Frequency')

    top_10_categories = filtered_df['product_category_name'].value_counts().nlargest(10)
    new_index = top_10_categories.index.str.replace('_', ' ')
    translated_index = new_index.map(lambda x: translator.translate(x, src='pt', dest='en').text)
    bar_fig_b = px.bar(top_10_categories, x=translated_index, y=top_10_categories.values, title='Top 10 Product Categories')
    bar_fig_b.update_layout(xaxis_title='Category', yaxis_title='Frequency')

    heatmap_data = filtered_df.groupby(['Weekday', 'Week_Number']).size().reset_index(name='Heat')
    day_dict = {i: day for i, day in enumerate(calendar.day_name)}
    heatmap_data['Weekday'] = heatmap_data['Weekday'].map(day_dict)
    day_list = list(calendar.day_name)
    heatmap_data['Weekday'] = pd.Categorical(heatmap_data['Weekday'], categories=day_list, ordered=True)
    heat_map = px.imshow(heatmap_data.pivot_table('Heat', 'Weekday', 'Week_Number'), title="Heatmap of Order Frequency by Weekday and Week Number")
    heat_map.update_layout(xaxis_title='Week Number')

    filtered_df['order_approved_at'] = pd.to_datetime(filtered_df['order_approved_at'])
    filtered_df['order_purchase_timestamp'] = pd.to_datetime(filtered_df['order_purchase_timestamp'])
    filtered_df['time_diff_a'] = (filtered_df['order_approved_at'] - filtered_df['order_purchase_timestamp']).dt.total_seconds() / 60
    filtered_df['time_diff_b'] = (filtered_df['order_delivered_customer_date'] - filtered_df['order_approved_at']).dt.total_seconds() / 60 / 60 / 24

    total_number_of_orders = filtered_df['order_id'].nunique()
    average_review_score = round(filtered_df['review_score'].mean(), 2)
    average_response_time = round(filtered_df['time_diff_a'].mean(), 2)
    average_delivery_time = round(filtered_df['time_diff_b'].mean(), 2)
    total_transaction_value = filtered_df['payment_value'].sum()
    total_number_of_customers = filtered_df['customer_unique_id'].nunique()
    total_number_of_sellers = filtered_df['seller_id'].nunique()
    average_transaction_value = round(total_transaction_value/total_number_of_customers, 2)
    total_transaction_value = round(total_transaction_value/1000, 2)

    return scatter_fig, pie_fig, bar_fig_a, bar_fig_b, heat_map, total_number_of_orders, average_review_score, average_response_time, average_delivery_time, total_transaction_value, average_transaction_value, total_number_of_customers, total_number_of_sellers

if __name__ == '__main__':
    app.run_server(debug=False)