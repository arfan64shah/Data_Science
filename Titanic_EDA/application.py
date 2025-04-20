# import the required libraries
import streamlit as st
import pandas as pd
import joblib as jb


# now load the saved model
model = jb.load('knn_titanic_model.joblib')

# titles
st.title('Predicting Titanic Surived People')
st.write('Enter Passenger Details Below')

# input fields
Pclass = st.selectbox('Passenger Class', [1, 2, 3])
Age = st.slider('', 0, 100, 20)
SibSp = st.number_input('Number of Siblings', min_value = 0, max_value = 10, value = 0)
Parch = st.number_input('Number of Parents', min_value = 0, max_value = 10, value = 0)
Fare = st.number_input('Fare', min_value=0.0, max_value=500.0, value=50.0)
Has_Cabin = st.selectbox("Has Cabin?", ["yes", "no"])
Sex_female = st.selectbox("Sex_female", [1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
Sex_male = st.selectbox("Is Male?", ["yes", "no"])
Embarked_C = st.selectbox("Embarked C?", ["yes", "no"])
Embarked_Q = st.selectbox("Embarked Q?", ["yes", "no"])
Embarked_S = st.selectbox("Embarked S?", ["yes", "no"])
Titles_Capt = st.selectbox("Is Capt?", ["yes", "no"])
Titles_Col = st.selectbox("Is Col?", ["yes", "no"])
Titles_Countess = st.selectbox("Is Countess?", ["yes", "no"])
Titles_Don = st.selectbox("Is Don?", ["yes", "no"])
Titles_Dr = st.selectbox("Is Dr?", ["yes", "no"])
Titles_Jonkheer = st.selectbox("Is Jonkheer?", ["yes", "no"])
Titles_Lady = st.selectbox("Is Lady?", ["yes", "no"])
Titles_Major = st.selectbox("Is Major?", ["yes", "no"])
Titles_Master = st.selectbox("Is Master?", ["yes", "no"])
Titles_Miss = st.selectbox("Is Miss?", ["yes", "no"])
Titles_Mlle = st.selectbox("Is Mlle?", ["yes", "no"])
Titles_Mme = st.selectbox("Is Mme?", ["yes", "no"])
Titles_Mr = st.selectbox("Is Mr?", ["yes", "no"])
Titles_Mrs = st.selectbox("Is Mrs?", ["yes", "no"])
Titles_Ms = st.selectbox("Is Ms?", ["yes", "no"])
Titles_Rev = st.selectbox("Is Rev?", ["yes", "no"])
Titles_Sir = st.selectbox("Is Sir?", ["yes", "no"])

# create a dataframe from input
input_data = pd.DataFrame({
    'Pclass': [Pclass],
    'Age': [Age],
    'SibSp': [SibSp],
    'Parch': [Parch],
    'Fare': [Fare],
    'Has_Cabin': [Has_Cabin],
    'Sex_female': [Sex_female],
    'Sex_male': [Sex_male],
    'Embarked_C': [Embarked_C],
    'Embarked_Q': [Embarked_Q],
    'Embarked_S': [Embarked_S],
    'Titles_Capt': [Titles_Capt],
    'Titles_Col': [Titles_Col],
    'Titles_Countess': [Titles_Countess],
    'Titles_Don': [Titles_Don],
    'Titles_Dr': [Titles_Dr],
    'Titles_Jonkheer': [Titles_Jonkheer],
    'Titles_Lady': [Titles_Lady],
    'Titles_Major': [Titles_Major],
    'Titles_Master': [Titles_Master],
    'Titles_Miss': [Titles_Miss],
    'Titles_Mlle': [Titles_Mlle],
    'Titles_Mme': [Titles_Mme],
    'Titles_Mr': [Titles_Mr],
    'Titles_Mrs': [Titles_Mrs],
    'Titles_Ms': [Titles_Ms],
    'Titles_Rev': [Titles_Rev],
    'Titles_Sir': [Titles_Sir]
})

# predict button
if st.button('Predict'):

    # make prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0]

    # disply result
    if prediction[0] == 1:
        st.success("The passenger can survive!")
    else:
        st.error("Unortunately the passenger can't survive!")
    
    st.write(f"Probability of survival: {probability[1]: 0.2%}")
    st.write(f"Probability of non-survival: {probability[0]: 0.2%}")