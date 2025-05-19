import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Визуализации", page_icon="📈", layout="wide")

CAPTIONS = {
    "duration_on_daytime.png": "Зависимость длительности поездки от времени суток",
    "duration_on_distance.png": "Влияение расстояния поездки на продолжительность",
    "duration_on_vendor.png": "Зависимость длительности от перевозчика",
    "duration_on_weekday.png": "Зависимость целевого признака от фактора: будни или выходные",
}

st.title("Визуализации зависимостей в данных")
st.write("Ниже представленные графики, показывающие влияние различных факторов на целевую переменную")

try:
    images = [f for f in os.listdir("images/vis") if f.endswith((".png", ".jpg"))]
    images.sort()
    
    cols = st.columns(2)
    
    for idx, img_file in enumerate(images):
        with cols[idx % 2]:
            c = st.container(height=500)
            img_path = os.path.join("images/vis", img_file)
            image = Image.open(img_path)
            
            c.image(image, use_container_width=False)
 
            caption = CAPTIONS.get(img_file, img_file.split(".")[0])
            c.caption(f"Рис. {idx+1}: {caption}")

except FileNotFoundError:
    st.error("Папка images не найдена!")
except Exception as e:
    st.error(f"Ошибка загрузки изображений: {str(e)}")
