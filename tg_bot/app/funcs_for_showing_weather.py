from web_app.make_plot import make_plot_from_2_dfs
from web_app.number_funcs import is_valid_coordinates
from web_app.open_meteo_connection import give_condition_df_from_open_meteo, convert_city_to_lat_lon


def make_weather_picture(lat_1, lon_1, lat_2, lon_2, time, param, path, name_1, name_2):
    condition_df_1 = give_condition_df_from_open_meteo(lat_1, lon_1, time)
    condition_df_2 = give_condition_df_from_open_meteo(lat_2, lon_2, time)
    fig = make_plot_from_2_dfs(condition_df_1, condition_df_2, param, name_1, name_2)
    print('picture saving...')
    fig.write_image(path)
    print('...picture saved')


def make_weather_picture_for_points(point_1, point_2, time, param, path):
    try:
        lat_1, lon_1 = map(float, point_1.split())
        lat_2, lon_2 = map(float, point_2.split())
        if not is_valid_coordinates(lat_1, lon_1) or not is_valid_coordinates(lat_2, lon_2):
            return "Неверно введены координаты"
    except:
        return "Неверно введены координаты"
    try:
        make_weather_picture(lat_1, lon_1, lat_2, lon_2,
                             time, param, path, 'Точка 1', 'Точка 2')
        return ""
    except:
        return "Не удалось создать картинку / проблемы с API"


def make_weather_picture_for_cities(city_1, city_2, time, param, path):
    lat_1, lon_1, name_1 = convert_city_to_lat_lon(city_1)
    lat_2, lon_2, name_2 = convert_city_to_lat_lon(city_2)
    if lat_1 is None or lat_2 is None:
        return "Невеозможно определить город"
    try:
        make_weather_picture(lat_1, lon_1, lat_2, lon_2,
                             time, param, path, name_1, name_2)
        return ""
    except:
        return "Не удалось создать картинку / Проблемы с API"


if __name__ == "__main__":
    make_weather_picture_for_points('15 12',
                                    '13 13',
                                    '3 дня',
                                    'Temperature',
                                    'test.png')
