import requests
import os
import streamlit as st

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

def get_table_from_supabase(table_name, params):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    # params = dict(select="*")
    headers = dict(
        apikey=SUPABASE_KEY,
        Authorization=f"Bearer {SUPABASE_KEY}")
    response = requests.get(url, params,
                            headers=headers)
    data = response.json()
    return data

params = dict(
    select='created_at',
    order='created_at.desc',
    dist='created_at',
)
st.write(get_table_from_supabase('momentum_score', params))