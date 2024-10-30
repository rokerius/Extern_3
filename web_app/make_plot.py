import numpy as np
import pandas as pd
import plotly.express as px

# Чтобы на графиках были красивые названия параметров
normal_names = {
    "temperature": "Температура (°C)",
    "humidity": "Влажность (%)",
    "precipitation": "Осадки (мм)",
    "wind_speed": "Скорость ветра (км/ч)"
}


# Создание графика по одной точке
def make_plot_from_df(df, full_name, params_cond):
    try:
        fig = px.line(df, x='date', y=params_cond)

        fig.update_layout(
            title=dict(text=full_name, font=dict(size=24), x=0.5),
            xaxis_title='Дата',
            yaxis_title=normal_names[params_cond],
            hovermode="x unified",
            template='plotly_white'
        )
        return fig
    except:
        return None


# Создание графика по двум точкам
def make_plot_from_2_dfs(df_1, df_2, param, name_1, name_2):
    try:
        fig = px.line()

        fig.add_scatter(x=df_1['date'], y=df_1[param], mode='lines', name=name_1)
        fig.add_scatter(x=df_2['date'], y=df_2[param], mode='lines', name=name_2)

        fig.update_layout(
            title=dict(text=f"{normal_names[param]} в двух точках",
                       font=dict(size=24), x=0.5),
            xaxis_title='Дата',
            yaxis_title=normal_names[param],
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        )
        return fig
    except:
        return None


if __name__ == "__main__":
    date_range_1 = pd.date_range(start='2023-01-01', periods=5, freq='D')
    date_range_2 = pd.date_range(start='2023-01-01', periods=5, freq='D')

    # Генерация случайных температур
    np.random.seed(0)
    temperatures_1 = np.random.randint(low=-10, high=35, size=5)
    temperatures_2 = np.random.randint(low=-10, high=35, size=5)

    df_1 = pd.DataFrame({
        'date': date_range_1,
        'temperature': temperatures_1
    })

    df_2 = pd.DataFrame({
        'date': date_range_2,
        'temperature': temperatures_2
    })

    fig = make_plot_from_2_dfs(df_1, df_2, 'temperature', 'Пупа', 'Лупа')
    fig.show()
    print('picture_saved')
