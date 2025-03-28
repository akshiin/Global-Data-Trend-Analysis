import streamlit as st
import pandas as pd

from utils import chow_test, get_connection, fast_insert

st.set_page_config(layout="wide")

st.title("Upload Data & Calculate Trends with Chow Test")

st.write("Download the empty template, fill in your data, and upload it to analyze trends.")

columns = [
    "Year", "Sector", "Subsector", "Indicator", "Country", 
    "Country_code", "Amount", "Rank"
]

template_df = pd.DataFrame(columns=columns)

csv = template_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Template",
    data=csv,
    file_name="data_template.csv",
    mime="text/csv"
)

st.divider()

st.subheader("Upload Your Data")

uploaded_file = st.file_uploader("Upload a filled CSV file", type=["csv"])

if uploaded_file is not None:

    user_data = pd.read_csv(uploaded_file)

    if set(columns) == set(user_data.columns):

        st.success("File uploaded successfully! Saving to the database...")
        st.success("Data successfully saved!")
        
        st.dataframe(user_data.head())

    else:
        st.error("The uploaded file does not match the required template. Please check the column names and try again.")

    
    df = user_data.copy()
    
    if st.button("Calculate Trend"):
        
        with st.spinner("⚙️ Processing Chow Test...", show_time=True):
            
            indicators, countries = [], []
            results = {f"chow_test_result_{bp}": [] for bp in [3, 5, 10]}
            results.update({f"p_value_{bp}": [] for bp in [3, 5, 10]})
            results.update({f"coeff_before_{bp}": [] for bp in [3, 5, 10]})
            results.update({f"coeff_after_{bp}": [] for bp in [3, 5, 10]})

            for indicator in df['Indicator'].unique():
                indicator_data = df[df['Indicator'] == indicator]
                for country in indicator_data['Country'].unique():
                    country_data = indicator_data[indicator_data['Country'] == country].sort_values("Year")

                    try:
                        scores = [chow_test(country_data, bp) for bp in [3, 5, 10]]
                        indicators.append(indicator)
                        countries.append(country)
                        
                        for i, bp in enumerate([3, 5, 10]):
                            results[f"chow_test_result_{bp}"].append(scores[i][0])
                            results[f"p_value_{bp}"].append(scores[i][1])
                            results[f"coeff_before_{bp}"].append(scores[i][2])
                            results[f"coeff_after_{bp}"].append(scores[i][3])
                    except:
                        continue

        test_results_df = pd.DataFrame({
            'Country': countries, 'Indicator': indicators, **results
        })

        final_df = df.merge(test_results_df, on=['Country', 'Indicator'], how='left')

        conn = get_connection()
        cursor = conn.cursor()

        create_table_query = """
        DROP TABLE IF EXISTS countries;
        CREATE TABLE countries (
            id SERIAL PRIMARY KEY,
            year INTEGER,
            sector TEXT,
            subsector TEXT,
            indicator TEXT,
            country TEXT,
            country_code TEXT,
            amount NUMERIC,
            rank NUMERIC,
            chow_test_result_3 NUMERIC,
            p_value_3 NUMERIC,
            coeff_before_3 NUMERIC,
            coeff_after_3 NUMERIC,
            chow_test_result_5 NUMERIC,
            p_value_5 NUMERIC,
            coeff_before_5 NUMERIC,
            coeff_after_5 NUMERIC,
            chow_test_result_10 NUMERIC,
            p_value_10 NUMERIC,
            coeff_before_10 NUMERIC,
            coeff_after_10 NUMERIC
        );
        """

        cursor.execute(create_table_query)
        conn.commit()

        st.success("✅ Table 'countries' created successfully!")

        final_df = final_df[[
            "Year", "Sector", "Subsector", "Indicator", "Country", "Country_code", "Amount", "Rank", 
            "chow_test_result_3", "chow_test_result_5", "chow_test_result_10", "p_value_3", "p_value_5", "p_value_10", 
            "coeff_before_3", "coeff_before_5", "coeff_before_10", "coeff_after_3", "coeff_after_5", "coeff_after_10"
        ]]

        with st.spinner("⚙️ Saving data to the database...", show_time=True):
            
            fast_insert(final_df)

            cursor.close()
            conn.close()

        st.success("✅ Chow Test Calculated & Data Saved to New Database!")

        st.dataframe(final_df.head(10))
