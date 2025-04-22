import streamlit as st
import pandas as pd
import joblib as jb

# Load the model
model = jb.load('knn_titanic_model.joblib')

# Custom CSS for compact layout
st.markdown("""
    <style>
    /* Reduce padding and margins for inputs */
    .stSelectbox, .stNumberInput, .stButton {
        margin-bottom: 5px !important;
        padding: 2px !important;
    }
    /* Smaller font size for labels */
    .stSelectbox label, .stNumberInput label {
        font-size: 12px !important;
    }
    /* Compact container */
    .stContainer, .stForm {
        padding: 10px !important;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    /* Reduce width of selectboxes */
    .stSelectbox > div > div {
        width: 150px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Titles
st.title('Titanic Survival Prediction')
st.write('Enter Passenger Details')

# Form to group inputs
with st.form(key="titanic_form"):
    # Passenger Info Section
    with st.expander("Passenger Info", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            Pclass = st.selectbox('Class', [1, 2, 3], help="Passenger class")
            Age = st.number_input('Age', min_value=10, max_value=100, value=10, step=1)
            SibSp = st.number_input('Siblings', min_value=0, max_value=10, value=0, step=1)
        with col2:
            Parch = st.number_input('Parents', min_value=0, max_value=10, value=0, step=1)
            Fare = st.number_input('Fare', min_value=0.0, max_value=500.0, value=50.0, step=0.1)
            Has_Cabin = st.selectbox("Cabin", ['Yes', 'No'], help="Has a cabin?")

    # Categorical Inputs Section
    with st.expander("Passenger Details", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            Gender = st.selectbox("Gender", ['Female', 'Male'])
            Embarked = st.selectbox("Embarked", ['Cherbourg', 'Queenstown', 'Southampton'])
        with col4:
            Title = st.selectbox("Title", [
                'Mr', 'Mrs', 'Miss', 'Master', 'Dr', 'Rev', 'Col', 'Major', 'Capt',
                'Countess', 'Don', 'Jonkheer', 'Lady', 'Mlle', 'Mme', 'Ms', 'Sir'
            ])

    # Submit button
    submit = st.form_submit_button("Predict")

# Process inputs and make prediction
if submit:
    # Map dropdown values to model input
    sex_female = 1 if Gender == 'Female' else 0
    sex_male = 1 if Gender == 'Male' else 0
    embarked_C = 1 if Embarked == 'Cherbourg' else 0
    embarked_Q = 1 if Embarked == 'Queenstown' else 0
    embarked_S = 1 if Embarked == 'Southampton' else 0
    has_cabin = 1 if Has_Cabin == 'Yes' else 0

    # Initialize title columns (all 0 except the selected title)
    titles = [
        'Capt', 'Col', 'Countess', 'Don', 'Dr', 'Jonkheer', 'Lady', 'Major',
        'Master', 'Miss', 'Mlle', 'Mme', 'Mr', 'Mrs', 'Ms', 'Rev', 'Sir'
    ]
    title_values = {f'Titles_{title}': 1 if Title == title else 0 for title in titles}

    # Create DataFrame
    input_data = pd.DataFrame({
        'Pclass': [Pclass],
        'Age': [Age],
        'SibSp': [SibSp],
        'Parch': [Parch],
        'Fare': [Fare],
        'Has_Cabin': [has_cabin],
        'Sex_female': [sex_female],
        'Sex_male': [sex_male],
        'Embarked_C': [embarked_C],
        'Embarked_Q': [embarked_Q],
        'Embarked_S': [embarked_S],
        **title_values
    })

    # Make prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0]

    # Display result
    if prediction[0] == 1:
        st.success("The passenger may survive!")
    else:
        st.error("The passenger may not survive!")
    
    st.write(f"Survival Probability: {probability[1]:.2%}")
    st.write(f"Non-Survival Probability: {probability[0]:.2%}")