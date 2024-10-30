from dash import Dash, html, dcc, callback, Output, Input, Patch, ALL
import dash_bootstrap_components as dbc
from open_meteo_connection import give_condition_df, convert_cities_to_df
from make_plot import make_plot_from_df
from world_map import create_world_map

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

cities = []

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Погода", className="text-center"), width=12)
    ], className="mb-4 pt-4"),

    html.Div(id='city-inputs-container'),

    dbc.Row([
        dbc.Col(dbc.Button("Добавить город", id="add-btn", n_clicks=0,
                           className="btn btn-light"), width="auto"),
    ], className="mb-3", justify='center'),

    dbc.Row([
        dbc.Col(dcc.RadioItems([' 1 Day', ' 3 Days', ' 7 Days', ' 14 Days'],
                               ' 3 Days',
                               id='params_time',
                               inline=True,
                               labelStyle={'display': 'block'}),
                width=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            options=[
                {'label': 'Temperature (Температура)', 'value': 'temperature'},
                {'label': 'Humidity (Влажность)', 'value': 'humidity'},
                {'label': 'Precipitation (Осадки)', 'value': 'precipitation'},
                {'label': 'Wind speed (Скорость ветра)', 'value': 'wind_speed'}
            ],
            value='temperature',
            id='params_cond',
            style={'width': '100%'}
        ), width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Button("Открыть/скрыть карту с введенными городами", id="show_map", n_clicks=0,
                           className="btn btn-primary"), width="auto")
    ], className="mb-1", justify='center'),

    html.Div(
        className='container mt-1 mb-5',
        children=[
            html.P('Погода представленная на карте является погодой в данный момент',
                   className="text-muted text-center sm"),
            html.Div(id='world_map', className='border rounded shadow')
            ]),

    html.Div(id='city-outputs-container')
], fluid=True)


@callback(
    Output("world_map", "children"),
    Input("show_map", "n_clicks")
)
def display_city_inputs(n_clicks):
    if n_clicks % 2 == 1:
        try:
            df_cities = convert_cities_to_df(cities)
            return dcc.Graph(figure=create_world_map(df_cities))
        except:
            return ""
    return ""


@callback(
    Output("city-inputs-container", "children"),
    Input("add-btn", "n_clicks")
)
def display_city_inputs(n_clicks):
    patched_children = Patch()
    new_input = dcc.Input(
        placeholder='Введите город',
        type='text',
        value='',
        id={'type': 'city-input', 'index': n_clicks},
        style={'width': '100%', 'marginBottom': '10px'}  # Full width input
    )
    patched_children.append(new_input)
    return patched_children


@callback(
    Output("city-outputs-container", "children"),
    Input({"type": "city-input", "index": ALL}, "value"),
    Input("params_time", "value"),
    Input('params_cond', "value"),
)
def display_output(city_values, params_time, params_cond):
    global cities
    cities = city_values
    graphs = []
    for i, city in enumerate(city_values):
        if city:
            df, full_name = give_condition_df(city, int(params_time.split()[0]))
            if not df is None:
                graph = make_plot_from_df(df, full_name, params_cond)
                graphs.append(dcc.Graph(id={'type': 'graph', 'index': i}, figure=graph))
    return html.Div(graphs)


if __name__ == '__main__':
    app.run(debug=True)
