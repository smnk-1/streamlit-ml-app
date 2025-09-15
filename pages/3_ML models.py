import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from preprocessing import *
import math

st.set_page_config(page_title="Model Selector", layout="wide")

st.title("Выбор и применение ML-модели")

# Словарь с моделями и путями
MODEL_PATHS = {
    "Линейная регрессия": "models/l1r.pkl",
    "Бустинг": "models/boost.pkl",
    "Бэггинг регрессор": "models/bag_regr.pkl",
    "Cтэкинг": "models/stack.pkl",
    "Полносвязная нейронная сеть": "models/fcnn copy.pkl"
}

# Кешируем загрузку моделей
@st.cache_resource
def load_model(model_path):
    return joblib.load(model_path)

# Загрузка всех моделей в словарь
models_cache = {}
for name, path in MODEL_PATHS.items():
    try:
        models_cache[name] = load_model(path)
        # st.success(f"Модель '{name}' успешно загружена")
    except Exception as e:
        st.warning(f"Не удалось загрузить модель '{name}': {str(e)}")

st.header("Выбор моделей")
selected_models = st.multiselect(
    "Выберите модели для предсказания",
    options=list(MODEL_PATHS.keys()),
    default=list(MODEL_PATHS.keys())[0]
)

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
    if not selected_models:
        st.warning("Пожалуйста, выберите хотя бы одну модель.")
        st.stop()
    
    try:
        processed_data = preprocess(data.copy())
    except Exception as e:
        st.error(f"Ошибка при предобработке данных: {e}")
        st.stop()
    
    results = {}
    for model_name in selected_models:
        if model_name not in models_cache:
            st.error(f"Модель '{model_name}' недоступна для предсказания")
            continue
            
        try:
            model = models_cache[model_name]
            predictions = model.predict(processed_data)
            results[model_name] = predictions
        except Exception as e:
            st.error(f"Ошибка при предсказании моделью '{model_name}': {e}")
    
    if results:
        st.success("Предсказания успешно выполнены")
        st.subheader("Результаты предсказаний")
        
        # Создаем DataFrame для отображения результатов
        results_df = pd.DataFrame()
        
        for model_name, preds in results.items():
            results_df[model_name] = [p for p in preds]
        
        # Добавляем индекс объектов
        results_df.index = [f"Объект {i+1}" for i in range(len(results_df))]
        
        # Отображаем таблицу с результатами
        st.dataframe(results_df.style.format("{:,.2f} s"))
        
    else:
        st.warning("Нет результатов для отображения")