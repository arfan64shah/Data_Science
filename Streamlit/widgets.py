# import required libraries
import streamlit as st

# title
st.title("Visualization Dashboard")

# drop down list
st.selectbox("Select Classification Type:", ('Binary Classification', 'Multi-Class Classification'))
st.button("Submit")

# radio button to chose types of classes
st.radio("Types of Classes:", ['Healthy', 'Early Blight', 'Late Blight'])

# select multiple options at a time
st.multiselect("Chose your course:", ['Data Science', 'Machine Learning', 'Statistics'])

# select slider
st.select_slider("Ratings: ", ['Bad', 'Good', 'Very Good', 'Excellent'])

# slider
st.slider('Slider:', 0, 10)