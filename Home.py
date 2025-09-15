import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Taxi ML-App",
    page_icon="👨‍💻")

st.title("Когда будет моё такси?")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("Данное приложение использует модели машинного обучения для предсказания времени поездки на такси.")
    st.write("Модели ML были обучены на данных множества поездок на такси в Нью-Йорке. Признаки датасета описаны подробнее на странице **Dataset Information**.")
    st.write("Перед обучением моделей была провдена предобработка данных и выявлены основные зависимости между признаками. Графики, отражающие зависимости представлены на странице **Visualisation**.")

with col2:
    try:
        image = Image.open('images/taxi-stock-image.jpg')

        st.image(image, width=300)
    except:
        st.warning("Фото не найдено!")

st.divider()

st.header("Информация о разработчике")
col1, col2 = st.columns([1, 2])

with col1:
    try:
        image = Image.open('images/person_photo.png')

        st.image(image, width=300)
    except:
        st.warning("Фото не найдено!")

with col2:
    st.write("**ФИО**: Семикин Николай Дмитриевич")
    st.write("**ВУЗ**: ОмГТУ (2023-2027)")
    st.write("**Факультет:** Факультет информационных технологий и компьютерных систем")
    st.write("**Специальность:** 02.03.02 Фундаментальная информатика")




st.divider()
st.header("Навигация:")
st.write("**Dataset information** -- страница, содеражая информацию о датасете, его предметной области, признаках и особенностях предобработки данных")
st.write("**Visualisation** -- предствление графиков, визуализирующих зависимости в данных")
st.write("**ML models** -- использование натренированных моделей на Ваших данных с возможностью выбора модели, ввода данных или загрузки датасета")

