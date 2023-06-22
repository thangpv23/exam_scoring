import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import cv2
import random
import numpy as np 
import os
import imutils
from imutils import contours
from PIL import Image, ImageTransform

from scoring_120 import exam120_scoring
from scoring_50 import exam50_scoring

st.title('Demo')


answer_key_120=[4, 2, 1, 1, 3, 4, 2, 3, 3, 1, 3, 2, 1, 2, 3, 1, 1, 4, 2, 2, 2, 1, 3, 3, 3, 4, 1, 1, 3, 1, 3, 1, 4, 1, 3, 2, 3, 1, 3, 1, 1, 2, 4, 2, 4, 2, 3, 4, 2, 2, 2, 2, 3, 3, 4, 1, 2, 4, 3, 4, 3, 4, 3, 4, 4, 4, 1, 1, 2, 2, 3, 3, 2, 4, 1, 4, 3, 1, 3, 1, 3, 2, 3, 2, 1, 3, 1, 3, 3, 3, 2, 1, 3, 1, 3, 2, 2, 3, 1, 4, 2, 3, 3, 3, 1, 2, 2, 4, 1, 1, 2, 2, 4, 2, 4, 3, 2, 3, 2, 1]
answer_key_50=[1, 3, 1, 4, 4, 4, 4, 3, 2, 3, 2, 4, 4, 4, 2, 2, 1, 1, 1, 2, 4, 4, 3, 3, 1, 1, 2, 3, 2, 2, 3, 3, 3, 1, 2, 4, 3, 1, 3, 1, 1, 1, 4, 4, 4, 2, 2, 3, 1, 2]

tmp_key_list_120 =[]
tmp_key_list_50 =[]

for i in range(120):
    if answer_key_120[i] == 1:
        tmp_key_list_120.append("A")
    elif answer_key_120[i] == 2:
        tmp_key_list_120.append("B")
    elif answer_key_120[i] == 3:
        tmp_key_list_120.append("C")
    elif answer_key_120[i] == 4:
        tmp_key_list_120.append("D")

for i in range(50):
    if answer_key_50[i] == 1:
        tmp_key_list_50.append("A")
    elif answer_key_50[i] == 2:
        tmp_key_list_50.append("B")
    elif answer_key_50[i] == 3:
        tmp_key_list_50.append("C")
    elif answer_key_50[i] == 4:
        tmp_key_list_50.append("D")

st.subheader('120-question type')


if st.button('Random other 120 keys'):
    answer_key_120 = []
    tmp_key_list_120 =[]

    for i in range(120):
        
        tmp_key = random.randrange(1, 5,1)
        answer_key_120.append(tmp_key)
        if tmp_key == 1:
            tmp_key = "A"
        elif tmp_key == 2:
            tmp_key = "B"
        elif tmp_key == 3:
            tmp_key = "C"
        elif tmp_key == 4:
            tmp_key = "D"
        tmp_key_list_120.append(tmp_key)

st.write("Answer key:")

tmp_key_list_120 = np.array(tmp_key_list_120)
tmp_key_list_120 = np.reshape(tmp_key_list_120,(1, 120))
df = pd.DataFrame( tmp_key_list_120, columns=('Question %d' % (i+1) for i in range(120)),)
st.dataframe(df, hide_index = True)
        

uploaded_file_120 = st.file_uploader("Upload 120 type")

if uploaded_file_120 is not None:
    # To read file as bytes:
    file_bytes = np.asarray(bytearray(uploaded_file_120.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    score, result_img = exam120_scoring(opencv_image, answer_key_120)
    st.image(result_img)
    score = round(score*10, 2)
    st.write("Score 120: ", score, "/10")



st.subheader('50-question type')

if st.button('Random other 50 keys'):
    answer_key_50 = []
    tmp_key_list_50 =[]

    for i in range(120):
        
        tmp_key = random.randrange(1, 5,1)
        answer_key_50.append(tmp_key)
        if tmp_key == 1:
            tmp_key = "A"
        elif tmp_key == 2:
            tmp_key = "B"
        elif tmp_key == 3:
            tmp_key = "C"
        elif tmp_key == 4:
            tmp_key = "D"
        tmp_key_list_50.append(tmp_key)

st.write("Answer key:")
tmp_key_list_50 = np.array(tmp_key_list_50)
tmp_key_list_50 = np.reshape(tmp_key_list_50,(1, 50))
df = pd.DataFrame( tmp_key_list_50, columns=('Question %d' % (i+1) for i in range(50)),)
st.dataframe(df, hide_index = True)
        

uploaded_file_50 = st.file_uploader("Upload 50 type")

if uploaded_file_50 is not None:
    # To read file as bytes:
    file_bytes = np.asarray(bytearray(uploaded_file_50.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    score, result_img = exam50_scoring(opencv_image, answer_key_50)
    st.image(result_img)
    score = round(score*10, 2)
    st.write("Score 120: ", score, "/10")

