import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Custom CSS for a compact and attractive interface with minimized space above title and sidebar header
st.markdown("""
    <style>
    .main { 
        padding: 0rem 1rem 1rem 1rem; 
        margin-top: -2rem; 
    }
    .stSidebar { 
        width: 280px !important; 
        padding-top: 0rem; 
        margin-top: -1rem; 
    }
    h1 { 
        color: #1f77b4; 
        font-size: 1.8rem; 
        margin-bottom: 0.5rem; 
        margin-top: 0rem; 
    }
    .stSidebar h2 { 
        color: #ff7f0e; 
        font-size: 1.2rem; 
        margin: 0.5rem 0; 
        margin-top: 0rem; 
    }
    .stSelectbox, .stMultiSelect { margin-bottom: 0.5rem; }
    .stButton>button { background-color: #1f77b4; color: white; border-radius: 5px; }
    .stDataFrame { font-size: 0.9rem; }
    .stPlotlyChart { margin-top: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# Title of the dashboard
st.title("Vaccination Dashboard")

# Load the dataset
@st.cache_data
def load_data():
    try:
        return pd.read_excel("progress_data.xlsx")
    except FileNotFoundError:
        st.error("File 'progress_data.xlsx' not found. Ensure it is in the script's directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading 'progress_data.xlsx': {str(e)}")
        st.stop()

df = load_data()

# Clean column names
df.columns = [col.replace('(', '').replace(')', '').replace(' ', '_') for col in df.columns]

# Dynamically extract date ranges
date_columns = [col for col in df.columns if col.startswith(('Reg', 'Vac'))]
date_ranges = sorted(set(re.search(r'\d{1,2}_[A-Za-z]{3}-\d{1,2}_[A-Za-z]{3}', col).group() 
                        for col in date_columns if re.search(r'\d{1,2}_[A-Za-z]{3}-\d{1,2}_[A-Za-z]{3}', col)))
date_to_columns = {dr: [f'Reg{dr}', f'Vac{dr}'] for dr in date_ranges}

# Sidebar filters in a compact layout
with st.sidebar:
    st.header("Filters")
    col1, col2 = st.columns(2)
    with col1:
        ucs = sorted(df['UC'].unique())
        selected_uc = st.selectbox("UC", options=["All"] + ucs, key="uc")
    with col2:
        facilities = sorted(df['Epi_Mis_Facility_Name'].unique()) if selected_uc == "All" else sorted(df[df['UC'] == selected_uc]['Epi_Mis_Facility_Name'].unique())
        selected_facility = st.selectbox("Facility", options=["All"] + facilities, key="facility")
    
    vaccinators = sorted(df['VaccinatorName'].unique()) if selected_uc == "All" and selected_facility == "All" else sorted(df[(df['UC'] == selected_uc) & (df['Epi_Mis_Facility_Name'] == selected_facility)]['VaccinatorName'].unique())
    selected_vaccinator = st.selectbox("Vaccinator", options=["All"] + vaccinators, key="vaccinator")
    
    selected_date_ranges = st.multiselect("Date Range(s)", options=date_ranges, default=date_ranges, key="dates")
    if not selected_date_ranges:
        st.warning("No date ranges selected. Showing all.")
        selected_date_ranges = date_ranges

# Filter the dataset
filtered_df = df.copy()
if selected_uc != "All":
    filtered_df = filtered_df[filtered_df['UC'] == selected_uc]
if selected_facility != "All":
    filtered_df = filtered_df[filtered_df['Epi_Mis_Facility_Name'] == selected_facility]
if selected_vaccinator != "All":
    filtered_df = filtered_df[filtered_df['VaccinatorName'] == selected_vaccinator]

if filtered_df.empty:
    st.warning("No data for selected filters.")
    st.stop()

# Results in a compact layout
st.subheader("Summary")
cols = st.columns(len(selected_date_ranges))
for idx, date_range in enumerate(selected_date_ranges):
    reg_col, vac_col = date_to_columns[date_range]
    reg_total = filtered_df[reg_col].sum()
    vac_total = filtered_df[vac_col].sum()
    with cols[idx]:
        st.markdown(f"**{date_range.replace('_', ' ')}**")
        st.markdown(f"Reg: {reg_total:,}<br>Vac: {vac_total:,}", unsafe_allow_html=True)

# Filtered data and download in an expander
with st.expander("View Filtered Data"):
    table_columns = ['UC', 'Epi_Mis_Facility_Name', 'VaccinatorName']
    rename_dict = {}
    for date_range in selected_date_ranges:
        reg_col, vac_col = date_to_columns[date_range]
        table_columns.extend([reg_col, vac_col])
        rename_dict[reg_col] = f'Reg ({date_range.replace("_", " ")})'
        rename_dict[vac_col] = f'Vac ({date_range.replace("_", " ")})'
    st.dataframe(filtered_df[table_columns].rename(columns=rename_dict), height=200)
    st.download_button(
        label="Download Data",
        data=filtered_df[table_columns].rename(columns=rename_dict).to_csv(index=False),
        file_name="filtered_vaccination_data.csv",
        mime="text/csv"
    )

# Visualization
st.subheader("Registrations vs Vaccinations")
if filtered_df.empty:
    st.write("No data for visualization.")
else:
    chart_data = pd.DataFrame({'Date Range': [], 'Metric': [], 'Count': []})
    for date_range in selected_date_ranges:
        reg_col, vac_col = date_to_columns[date_range]
        chart_data = pd.concat([
            chart_data,
            pd.DataFrame({
                'Date Range': [date_range.replace('_', ' ')],
                'Metric': ['Registrations'],
                'Count': [filtered_df[reg_col].sum()]
            }),
            pd.DataFrame({
                'Date Range': [date_range.replace('_', ' ')],
                'Metric': ['Vaccinations'],
                'Count': [filtered_df[vac_col].sum()]
            })
        ], ignore_index=True)

    fig = px.bar(
        chart_data,
        x='Date Range',
        y='Count',
        color='Metric',
        barmode='group',
        title='',
        labels={'Count': 'Count', 'Date Range': ''},
        text='Count',
        height=350,
        color_discrete_map={'Registrations': '#1f77b4', 'Vaccinations': '#ff7f0e'}
    )
    fig.update_traces(textposition='outside', texttemplate='%{text:,}', textfont_size=10)
    fig.update_layout(
        showlegend=True,
        xaxis_title="",
        yaxis_title="Count",
        xaxis_tickangle=45,
        margin=dict(t=20, b=100, l=50, r=50),
        font=dict(size=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)