import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the dashboard
st.title("Vaccination Progress Dashboard")

# Load the dataset
@st.cache_data
def load_data():
    # In practice, replace this with the path to your Excel file
    # For this example, we'll assume the data is loaded from the provided dataset
    data = pd.read_excel("progress_data.xlsx")
    return data

df = load_data()

# Clean column names (remove spaces and special characters for easier handling)
df.columns = [col.replace('(', '').replace(')', '').replace(' ', '_') for col in df.columns]

# Define date range options for the filter
date_ranges = [
    '1 Mar-10 Mar',
    '11 Mar-20 Mar',
    '1 Apr-10 Apr',
    '11 Apr-20 Apr'
]

# Sidebar for filters
st.sidebar.header("Filters")

# UC filter
ucs = sorted(df['UC'].unique())
selected_uc = st.sidebar.selectbox("Select UC", options=["All"] + ucs)

# Facility filter (dependent on UC)
if selected_uc == "All":
    facilities = sorted(df['Epi_Mis_Facility_Name'].unique())
else:
    facilities = sorted(df[df['UC'] == selected_uc]['Epi_Mis_Facility_Name'].unique())
selected_facility = st.sidebar.selectbox("Select Facility", options=["All"] + facilities)

# Vaccinator filter (dependent on UC and Facility)
if selected_uc == "All" and selected_facility == "All":
    vaccinators = sorted(df['VaccinatorName'].unique())
elif selected_uc == "All":
    vaccinators = sorted(df[df['Epi_Mis_Facility_Name'] == selected_facility]['VaccinatorName'].unique())
elif selected_facility == "All":
    vaccinators = sorted(df[df['UC'] == selected_uc]['VaccinatorName'].unique())
else:
    vaccinators = sorted(df[(df['UC'] == selected_uc) & (df['Epi_Mis_Facility_Name'] == selected_facility)]['VaccinatorName'].unique())
selected_vaccinator = st.sidebar.selectbox("Select Vaccinator", options=["All"] + vaccinators)

# Date range filter (multi-select)
selected_date_ranges = st.sidebar.multiselect("Select Date Range(s)", options=date_ranges, default=date_ranges)

# Filter the dataset based on UC, facility, and vaccinator selections
filtered_df = df.copy()
if selected_uc != "All":
    filtered_df = filtered_df[filtered_df['UC'] == selected_uc]
if selected_facility != "All":
    filtered_df = filtered_df[filtered_df['Epi_Mis_Facility_Name'] == selected_facility]
if selected_vaccinator != "All":
    filtered_df = filtered_df[filtered_df['VaccinatorName'] == selected_vaccinator]

# Define columns for the date ranges
date_to_columns = {
    '1 Mar-10 Mar': ['Reg1_Mar-10_Mar', 'Vac1_Mar-10_Mar'],
    '11 Mar-20 Mar': ['Reg11_Mar-20_Mar', 'Vac11_Mar-20_Mar'],
    '1 Apr-10 Apr': ['Reg01_Apr-10_Apr', 'Vac01_Apr-10_Apr'],
    '11 Apr-20 Apr': ['Reg11_Apr-20_Apr', 'Vac11_Apr-20_Apr']
}

# Display results
st.header("Results")
if not selected_date_ranges:
    st.write("Please select at least one date range.")
else:
    for date_range in selected_date_ranges:
        reg_col, vac_col = date_to_columns[date_range]
        reg_total = filtered_df[reg_col].sum()
        vac_total = filtered_df[vac_col].sum()
        st.write(f"**{date_range}**")
        st.write(f"Total Registrations: {reg_total}")
        st.write(f"Total Vaccinations: {vac_total}")

# Display filtered data table
st.subheader("Filtered Data")
if not selected_date_ranges:
    st.write("No data to display. Please select at least one date range.")
else:
    # Prepare columns for the data table
    table_columns = ['UC', 'Epi_Mis_Facility_Name', 'VaccinatorName']
    rename_dict = {}
    for date_range in selected_date_ranges:
        reg_col, vac_col = date_to_columns[date_range]
        table_columns.extend([reg_col, vac_col])
        rename_dict[reg_col] = f'Registrations ({date_range})'
        rename_dict[vac_col] = f'Vaccinations ({date_range})'
    st.dataframe(filtered_df[table_columns].rename(columns=rename_dict))

# Visualization: Compare registrations and vaccinations for 1 Mar-10 Mar and 1 Apr-10 Apr
st.subheader("Visualization: Comparison of 1 Mar-10 Mar vs 1 Apr-10 Apr")

if not filtered_df.empty:
    # Calculate totals for the two date ranges
    mar_reg = filtered_df['Reg1_Mar-10_Mar'].sum()
    mar_vac = filtered_df['Vac1_Mar-10_Mar'].sum()
    apr_reg = filtered_df['Reg01_Apr-10_Apr'].sum()
    apr_vac = filtered_df['Vac01_Apr-10_Apr'].sum()

    # Create a DataFrame for the comparison
    chart_data = pd.DataFrame({
        'Date Range': ['1 Mar-10 Mar', '1 Mar-10 Mar', '1 Apr-10 Apr', '1 Apr-10 Apr'],
        'Metric': ['Registrations', 'Vaccinations', 'Registrations', 'Vaccinations'],
        'Count': [mar_reg, mar_vac, apr_reg, apr_vac]
    })

    # Create a grouped bar chart using Plotly
    fig = px.bar(
        chart_data,
        x='Date Range',
        y='Count',
        color='Metric',
        barmode='group',
        title='Registrations and Vaccinations: 1 Mar-10 Mar vs 1 Apr-10 Apr',
        labels={'Count': 'Count', 'Date Range': 'Date Range'}
    )
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected filters.")