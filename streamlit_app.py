import requests
import os
import streamlit as st
import pandas as pd
import math

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

@st.cache_data
def get_etfs():
    url = "https://finance.naver.com/api/sise/etfItemList.nhn"
    params = dict(
        etfType=0,
        targetColumn='market_sum',
        sortOrder='desc'
    )
    response = requests.get(url, params)
    data = response.json()['result']['etfItemList']
    return pd.DataFrame(data).iloc[:, [0, 2]]

st.set_page_config(
    page_title='Momentum Dashboard',
    page_icon='🕹️')

option = dict(
    label = "🌬️ Total",
    min_value = 0,
    step=1,
    value=80_000_000,
    key='total'
)
st.number_input(**option)

col1, col2 = st.columns([3, 2])

etfs = get_etfs()

with col1:
    table_name = 'recent_momentum_score'
    data = get_table_from_supabase(table_name)
    df = pd.DataFrame(data)
    df = pd.merge(df, etfs, left_on='symbol', right_on='itemcode')
    df.rename(columns={'name':'category'})
    st.dataframe(df.iloc[:10, [0, 1, -1]],
                 hide_index=True,
                 use_container_width=True)

with col2:
    df2 = df[df.score >= df.score.iloc[4]].query('score > 0')
    df2['unit'] = (((0.01 / df2.aatr) / 4 * st.session_state.total // 1000000).apply(math.floor) * 1000000)
    st.dataframe(df2.loc[:, ['symbol', 'unit']], hide_index=True, use_container_width=True)
    st.metric("위험 조정 후 주식 비중", f"{math.floor(df2.unit.sum() / st.session_state.total * 10000) / 100}%")

with st.expander("Cluster Groups"):
    table_name = 'recent_cluster_groups'
    data = get_table_from_supabase(table_name)
    df3 = pd.DataFrame(data)
    df3.cluster_name = df3.cluster_name.str.replace(".", "")
    df3['cluster_groups'] = df3['cluster_groups'].str.split(', ')
    st.dataframe(df3.iloc[:, [1,0]], hide_index=1, use_container_width=1,
    column_config={
        "cluster_name": "클러스터 그룹명",
        "cluster_groups": st.column_config.ListColumn("그룹별 종목")
    })

st.image('./welcome.png', use_column_width=1)