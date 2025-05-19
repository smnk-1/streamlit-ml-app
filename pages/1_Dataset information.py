import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Dataset Info", page_icon="📁")


st.title("Информация о датасете")
st.write("""
**Предметная область:** Данные о поездках нью-йоркских такси (Yellow Cab)  
**Целевая переменная:** `trip_duration` - продолжительность поездки в секундах  
""")

# Описание признаков
with st.expander("Описание признаков", expanded=True):
    features = {
        'Признак': ['id', 'vendor_id', 'pickup_datetime', 'passenger_count',
                'pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
                'dropoff_latitude', 'trip_duration'],
        'Тип данных': ['object', 'float64', 'object', 'int64', 'float64', 'float64',
                    'float64', 'float64', 'int64'],
        'Описание': [
            'Уникальный идентификатор поездки',
            'Идентификатор перевозчика',
            'Дата и время начала поездки',
            'Количество пассажиров',
            'Долгота точки посадки',
            'Широта точки посадки',
            'Долгота точки высадки',
            'Широта точки высадки',
            'Продолжительность поездки (целевая переменная)'
        ]
    }
    st.dataframe(pd.DataFrame(features), hide_index=True)

st.header("Визуализация координат датасета")
st.write("""
**Зеленые точки** -- точки посадки пассажиров  
**Красные точки** -- точки высадки пассажиров
""")

try:
    df_locations = pd.read_csv("data/coordinates.csv")
    
    pickup_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_locations[df_locations['type'] == 'pickup'],
        get_position='[lon, lat]',
        get_color='[0, 255, 0, 160]',
        get_radius=70,
        pickable=True
    )

    dropoff_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_locations[df_locations['type'] == 'dropoff'],
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 160]',
        get_radius=70,
        pickable=True
    )


    view_state = pdk.ViewState(
        latitude=40.74980545,
        longitude=-73.98129272,
        zoom=11,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[pickup_layer, dropoff_layer],
        tooltip={"html": "<b>Тип:</b> {type}<br><b>Координаты:</b> [{lat}, {lon}]"}
    ))

except FileNotFoundError:
    st.error("Файл с координатами не найден! Убедитесь в наличии файла data/coordinates.csv")
except Exception as e:
    st.error(f"Ошибка загрузки данных: {str(e)}")

st.header("Предобработка данных")
st.write("""
### Выполненные преобразования:
- Удаление дубликатов
- Устранение пропусков
- Обработка временных меток
- Кодирование категориальных признаков
- Обогащение данных
    - Добавление расстояния поездки по координатам
    - Добавление признака: в центре города / за городом
    - Добавление признака: час 
    - Добавление признака: поездка в будни / выходные
""")
