import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


# Carregar os dados

df = pd.read_csv("Output/Df_new.csv")

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state='collapsed',
    )


# Título
st.title('Previsão de Vendas')
