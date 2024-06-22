import streamlit as st
from PIL import Image
import random

# รูปภาพที่ใช้ในเกม
images = [
    'IMG_7403.jpeg', 'image2.jpg', 'image3.jpg'
]

# เริ่มต้นเกม
def play_matching_game():
    st.title('Trip Korat EP2')
    st.write('Select day for ')


    
    # แบ่งหน้าจอเป็นคอลัมน์ 4 คอลัมน์
    col1, col2, col3, col4 = st.columns(4)

    # แสดงรูปภาพในแต่ละคอลัมน์
    if col1.button('Day 1'):
        st.image(Image.open( 'IMG_7403.jpeg'), use_column_width=True)
    if col2.button('Day 2'):
        st.image(Image.open( 'image2.jpg'), use_column_width=True)
    if col3.button('Day 3'):
        st.image(Image.open( 'image3.jpg'), use_column_width=True)
  

    # if st.button('Reset'):
    #     play_matching_game()

# เรียกฟังก์ชันเริ่มต้นเกม
play_matching_game()
