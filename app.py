import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Global Data Trend Analysis App")

data = pd.read_csv("data.csv", index_col=False)

sector = st.sidebar.selectbox(
    label="Sector",
    options=list(data['Sector'].unique())
)

data = data.loc[data['Sector'] == sector].reset_index(drop=True)

subsector = st.sidebar.selectbox(
    label="Subsector",
    options=list(data['Subsector'].unique())
)

data = data.loc[data['Subsector'] == subsector].reset_index(drop=True)

indicator = st.sidebar.selectbox(
    label="Indicator",
    options=list(data['Indicator'].unique())
)

data = data.loc[data['Indicator'] == indicator].reset_index(drop=True)

year = st.sidebar.number_input(
    label="Year",
    min_value=int(data['Year'].min()),
    max_value=int(data['Year'].max()),
    value=int(data['Year'].max())
)

table_data = data.loc[data['Year'] == year].reset_index(drop=True)

top_countries = st.sidebar.number_input(
    label="Top N countries",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

table_data = table_data.sort_values(by='Rank', ascending=True).reset_index(drop=True).loc[:top_countries]

st.dataframe(data=table_data)

countries = st.multiselect(
    label="Countries",
    options=list(table_data['Country'].unique()),
    default=list(table_data['Country'].unique())
)

st.line_chart(
    data=data.loc[data['Country'].isin(countries)],
    x='Year',
    y='Amount',
    color="Country"
)