import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Global Data Trend Analysis App")

data = pd.read_csv("results.csv", index_col=False)

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

table_data = data.loc[data['Year'] == data['Year'].max()].reset_index(drop=True)

top_countries = st.sidebar.number_input(
    label="Top N countries",
    min_value=5,
    max_value=table_data['Rank'].max(),
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
    ).reset_index(drop=True).loc[:top_countries]

else:
    table_data = table_data.loc[
        (table_data[f'p_value_{bp}'] < 0.05) &
        (table_data[f'coeff_after_{bp}'] < 0)
    ].sort_values(
        by=f'chow_test_result_{bp}',
        ascending=False
    ).reset_index(drop=True).loc[:top_countries]

st.subheader(
    body=f"Top-{top_countries} {trend_type.lower()} countries in {indicator} indicator for the last {bp} years"
)

st.dataframe(
    data=table_data[[
        'Country', 'Indicator', 'Subsector',
        'Sector', 'Amount', f'chow_test_result_{bp}'
    ]],
    column_config={f'chow_test_result_{bp}': st.column_config.NumberColumn(format="%.2f")}
)

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