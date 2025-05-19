import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Информация о разработчике",
    page_icon="👨‍💻",
    layout="centered"
)

st.title("Информация о разработчике")

col1, col2 = st.columns([1, 2])

with col1:
    try:
        image = Image.open('images/person_photo.png')

        st.image(image, width=300)
    except:
        st.warning("Фото не найдено!")

with col2:
    st.subheader("ФИО: Семикин Николай Дмитриевич")
    st.subheader("Группа: ФИТ-232")

st.divider()
st.header("📚 **РАСЧЕТНО-ГРАФИЧЕСКАЯ РАБОТА**")
st.write("по дисциплине: **«МАШИННОЕ ОБУЧЕНИЕ И БОЛЬШИЕ ДАННЫЕ»**")
st.write("Тема: «Разработка Web-приложения (дашборда) для инференса (вывода) моделей ML и анализа данных»")

st.divider()
st.header("Навигация:")
st.write("**Dataset information** -- страница, содеражая информацию о датасете, его предметной области, признаках и особенностях предобработки данных")
st.write("**Visualisation** -- предствление графиков, визуализирующих зависимости в данных")
st.write("**ML models** -- использование натренированных моделей на Ваших данных с возможностью выбора модели, ввода данных или загрузки датасета")
