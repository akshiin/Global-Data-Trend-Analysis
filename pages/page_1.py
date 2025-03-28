import streamlit as st
import pandas as pd

from utils import get_connection

st.set_page_config(layout="wide")

st.title("Global Data Trend Analysis App")

st.divider()

conn = get_connection()
cursor = conn.cursor()

data = pd.read_sql("SELECT * FROM countries", conn)
data.drop('id', axis=1, inplace=True)

cursor.close()
conn.close()

trend_type = st.sidebar.radio(
    label="Trend type",
    options=["Trending", "Downgrading"]
)

bp = st.sidebar.radio(
    label="Breakpoint (last N years)",
    options=[3, 5, 10]
)

sector = st.sidebar.selectbox(
    label="Sector",
    options=list(data['sector'].unique())
)

data = data.loc[data['sector'] == sector].reset_index(drop=True)

subsector = st.sidebar.selectbox(
    label="Subsector",
    options=list(data['subsector'].unique())
)

data = data.loc[data['subsector'] == subsector].reset_index(drop=True)

indicator = st.sidebar.selectbox(
    label="Indicator",
    options=list(data['indicator'].unique())
)

data = data.loc[data['indicator'] == indicator].reset_index(drop=True)

table_data = data.loc[data['year'] == data['year'].max()].reset_index(drop=True)

top_countries = st.sidebar.number_input(
    label="Top N countries",
    min_value=5,
    max_value=int(table_data['rank'].max()),
    value=10,
    step=5
)

if trend_type == "Trending":
    table_data = table_data.loc[
        (table_data[f'p_value_{bp}'] < 0.05) &
        (table_data[f'coeff_after_{bp}'] > 0)
    ].sort_values(
        by=f'chow_test_result_{bp}',
        ascending=False
    ).reset_index(drop=True).loc[:top_countries-1]

else:
    table_data = table_data.loc[
        (table_data[f'p_value_{bp}'] < 0.05) &
        (table_data[f'coeff_after_{bp}'] < 0)
    ].sort_values(
        by=f'chow_test_result_{bp}',
        ascending=False
    ).reset_index(drop=True).loc[:top_countries-1]

st.subheader(
    body=f"Top-{top_countries} {trend_type.lower()} countries in {indicator} indicator for the last {bp} years"
)

table_data.index = table_data.index + 1

st.dataframe(
    data=table_data[[
        'country', 'indicator', 'subsector',
        'sector', f'chow_test_result_{bp}'
    ]],
    column_config={f'chow_test_result_{bp}': st.column_config.NumberColumn(format="%.2f")}
)

countries = st.multiselect(
    label="Countries",
    options=list(table_data['country'].unique()),
    default=list(table_data['country'].unique())
)

st.line_chart(
    data=data.loc[data['country'].isin(countries)],
    x='year',
    y='amount',
    color="country"
)