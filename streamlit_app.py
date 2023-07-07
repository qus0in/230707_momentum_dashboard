import requests
import os
import streamlit as st
import pandas as pd

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

def get_table_from_supabase(table_name):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    params = dict(select="*")
    headers = dict(
        apikey=SUPABASE_KEY,
        Authorization=f"Bearer {SUPABASE_KEY}")
    response = requests.get(url, params,
                            headers=headers)
    data = response.json()
    return data

option = dict(
    label = "자산총액",
    min_value = 0,
    step=1,
    key='total'
)
st.number_input(**option)

col1, col2 = st.columns(2)

with col1:
    table_name = 'recent_momentum_score'
    data = get_table_from_supabase(table_name)
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=1, use_container_width=1)

with col2:
    df2 = df[df.score >= df.score.iloc[3]].query('score > 0')
    df2['Unit'] = (0.01 / df2.aatr) * st.session_state.total
    st.dataframe(df2.iloc[:, [0, 1, 4]], hide_index=1, use_container_width=1)