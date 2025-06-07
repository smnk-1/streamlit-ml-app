import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from preprocessing import *
import math

st.set_page_config(page_title="Model Selector", layout="wide")

st.title("Выбор и применение ML-модели")

model_options = {
    "Линейная регрессия": "models/l1r.pkl",
    "Бустинг": "models/boost.pkl",
    "Бэггинг регрессор": "models/bag_regr.pkl",
    "Cтэкинг": "models/stack.pkl",
    "Полносвязная нейронная сеть": "models/fcnn copy.pkl"
}

selected_name = st.selectbox("Выберите модель для предсказания", list(model_options.keys()))
model_path = model_options[selected_name]

st.header("Загрузка данных")
uploaded_file = st.file_uploader("Загрузите CSV-файл с данными", type="csv")

def manual_input():
    st.subheader("Ручной ввод признаков")
    cols = {}
    cols['vendor_id'] = st.selectbox("vendor_id", [1, 2], help="Идентификатор поставщика услуги")
    cols['pickup_datetime'] = st.date_input("Дата и время начала поездки", datetime.now())
    cols['pickup_time'] = st.time_input("Время начала поездки", datetime.now().time())
    cols['dropoff_datetime'] = st.date_input("Дата и время окончания поездки", datetime.now())
    cols['dropoff_time'] = st.time_input("Время окончания поездки", datetime.now().time())
    cols['passenger_count'] = st.number_input("Количество пассажиров", min_value=1, max_value=10, value=1)
    cols['pickup_longitude'] = st.number_input("Долгота точки старта", format="%.6f")
    cols['pickup_latitude'] = st.number_input("Широта точки старта", format="%.6f")
    cols['dropoff_longitude'] = st.number_input("Долгота точки окончания", format="%.6f")
    cols['dropoff_latitude'] = st.number_input("Широта точки окончания", format="%.6f")

    dt_start = datetime.combine(cols['pickup_datetime'], cols['pickup_time'])
    dt_end = datetime.combine(cols['dropoff_datetime'], cols['dropoff_time'])
    df = pd.DataFrame([{  
        'vendor_id': cols['vendor_id'],
        'pickup_datetime': dt_start,
        'dropoff_datetime': dt_end,
        'passenger_count': cols['passenger_count'],
        'pickup_longitude': cols['pickup_longitude'],
        'pickup_latitude': cols['pickup_latitude'],
        'dropoff_longitude': cols['dropoff_longitude'],
        'dropoff_latitude': cols['dropoff_latitude'],
    }])
    return df

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.write("### Предварительный просмотр данных")
        st.dataframe(data.head())
    except Exception as e:
        st.error(f"Ошибка при чтении CSV: {e}")
        st.stop()
else:
    data = manual_input()
    st.write("### Ваш ввод")
    st.dataframe(data)

if st.button("Получить предсказание"):
    try:
        model = joblib.load(model_path)
        data = preprocess(data)
        predictions = model.predict(data)
        st.success("Предсказание выполнено")
        for i, pred in enumerate(predictions):
            st.write(f"Объект {i+1}: {abs(pred):,.2f} s", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Файл модели '{model_path}' не найден. Убедитесь, что он находится в рабочей директории.")
    except Exception as e:
        st.error(f"Ошибка при предсказании: {e}")
