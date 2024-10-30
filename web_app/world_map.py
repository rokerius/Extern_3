import plotly.express as px

from web_app.open_meteo_connection import convert_cities_to_df


def create_world_map(df_cities):
    df_cities['info'] = df_cities['Город'] + "  (" + df_cities['Погода'] + ')'

    fig = px.line_map(df_cities, lat="lat", lon="lon", zoom=2, height=300, hover_name="Город", text="info")
    fig.update_traces(marker=dict(size=8), textposition='top center')
    fig.update_layout(map_style="open-street-map", map_zoom=2, map_center_lat=41,
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(textfont=dict(size=12, color='red', weight='bold'))

    return fig


if __name__ == "__main__":
    sities = ['Москва', 'Санкт-Петербург', 'Los Angeles', 'Бахмут', 'Киев']
    df_cities = convert_cities_to_df(sities)
    fig = create_world_map(df_cities)
    fig.show()