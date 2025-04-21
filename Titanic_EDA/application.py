# import the required libraries
import streamlit as st
import pandas as pd
import joblib as jb


# now load the saved model
model = jb.load('knn_titanic_model.joblib')

# titles
st.title('Predicting Titanic Survived People')
st.write('Enter Passenger Details Below')

# input fields
Pclass = st.selectbox('Passenger Class', [1, 2, 3])
Age = st.number_input('Age', min_value = 10, max_value = 100, value = 10)
SibSp = st.number_input('Number of Siblings', min_value = 0, max_value = 10, value = 0)
Parch = st.number_input('Number of Parents', min_value = 0, max_value = 10, value = 0)
Fare = st.number_input('Fare', min_value=0.0, max_value=500.0, value=50.0)
Has_Cabin = st.selectbox("Has_Cabin", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
Sex_female = st.selectbox("Sex_female", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
Sex_male = st.selectbox("Sex_male", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
Embarked_C = st.selectbox("Embarked_C", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Embarked_Q = st.selectbox("Embarked_Q", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Embarked_S = st.selectbox("Embarked_S", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Capt = st.selectbox("Titles_Capt", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Col = st.selectbox("Titles_Col", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Countess = st.selectbox("Titles_Countess", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Don = st.selectbox("Titles_Don", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Dr = st.selectbox("Titles_Dr", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Jonkheer = st.selectbox("Titles_Jonkheer", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Lady = st.selectbox("Titles_Lady", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Major = st.selectbox("Titles_Major", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Master = st.selectbox("Titles_Master", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Miss = st.selectbox("Titles_Miss", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Mlle = st.selectbox("Titles_Mlle", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Mme = st.selectbox("Titles_Mme", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Mr = st.selectbox("Titles_Mr", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Mrs = st.selectbox("Titles_Mrs", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Ms = st.selectbox("Titles_Ms", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Rev = st.selectbox("Titles_Rev", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")
Titles_Sir = st.selectbox("Titles_Sir", [1, 0], format_func=lambda x: "yes" if x == 1 else "No")

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