from deta import Deta
import streamlit as st


deta_key = st.secrets['deta_key']
db = Deta(deta_key)