import pandas as pd
import numpy as np
import psycopg2, io
import statsmodels.api as sm
from scipy.stats import f


def get_connection():
    conn = psycopg2.connect(
        "postgresql://neondb_owner:npg_XwzjiEP1MB3u@ep-dark-tree-a2izalir-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    )
    return conn


def fast_insert(df, batch_size=10000):
    conn = get_connection()
    cursor = conn.cursor()
    
    for i in range(0, len(df), batch_size):
        chunk = df.iloc[i:i+batch_size]
        output = io.StringIO()
        chunk.to_csv(output, sep='\t', index=False, header=False, na_rep='\\N')
        output.seek(0)
        cursor.copy_from(output, 'countries', sep='\t',
                         columns=["year", "sector", "subsector", "indicator", "country", "country_code", "amount", "rank", 
                                  "chow_test_result_3", "chow_test_result_5", "chow_test_result_10", "p_value_3", "p_value_5", "p_value_10", 
                                  "coeff_before_3", "coeff_before_5", "coeff_before_10", "coeff_after_3", "coeff_after_5", "coeff_after_10"])
        conn.commit()

    cursor.close()
    conn.close()
    print("Data inserted successfully in batches!")


def chow_test(data: pd.DataFrame, break_point: int):
    if len(data) <= break_point:
        return np.nan, np.nan, np.nan, np.nan  # Not enough data
    
    # Split the data
    data1, data2 = data.iloc[:-break_point], data.iloc[-break_point:]
    
    # Define dependent & independent variables
    y1, y2 = data1['Amount'], data2['Amount']
    X1, X2 = sm.add_constant(data1['Year']), sm.add_constant(data2['Year'])
    
    # Fit OLS models
    model1, model2 = sm.OLS(y1, X1).fit(), sm.OLS(y2, X2).fit()
    
    # Fit full dataset model
    X_full, y_full = sm.add_constant(data['Year']), data['Amount']
    model_full = sm.OLS(y_full, X_full).fit()
    
    # Compute Residual Sum of Squares (RSS)
    RSS1, RSS2, RSS_full = model1.ssr, model2.ssr, model_full.ssr
    
    # Compute Chow test statistic
    k, n1, n2 = 2, len(y1), len(y2)
    numerator = (RSS_full - (RSS1 + RSS2)) / k
    denominator = (RSS1 + RSS2) / (n1 + n2 - 2 * k)
    F_stat = numerator / denominator
    p_value = 1 - f.cdf(F_stat, k, n1 + n2 - 2 * k)
    
    return F_stat, p_value, np.round(model1.params.iloc[1], 5), np.round(model2.params.iloc[1], 5)