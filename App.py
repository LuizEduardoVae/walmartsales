import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Carregar os dados
df = pd.read_csv("Output/Df_new.csv")
avg_sales_per_store_department = df.groupby(['Date', 'Store', 'Dept'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store = df.groupby(['Store'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department['Date'] = pd.to_datetime(avg_sales_per_store_department['Date'])

# Configurações de cores
colors = {
    'background': '#0f1116',
    'text': '#17202A',
    'plot_color': '#5499C7',
    'section_title': '#1F618D',
    'highlight': '#E74C3C',
    'button_color': '#1ABC9C'
}

# Título
st.title('Análise de Vendas do Walmart')

# Subtítulo
st.sidebar.title('Analise Semanal de Vendas por Loja e Departamento')

# Selecione a loja
selected_store = st.sidebar.selectbox('Selecione a loja:', ['Média Geral'] + list(avg_sales_per_store_department['Store'].unique()))

# Seção: Análise de Departamentos
if selected_store == 'Média Geral':
    filtered_data_store = avg_sales_per_store_department
else:
    filtered_data_store = avg_sales_per_store_department[avg_sales_per_store_department['Store'] == selected_store]

selected_dept = st.sidebar.selectbox('Selecione o departamento que deseja analisar:', ['Média Geral'] + list(filtered_data_store['Dept'].unique()))
if selected_dept == 'Média Geral' and selected_store != 'Média Geral':
    filtered_data_dept = filtered_data_store.groupby('Date')['Weekly_Sales'].mean().reset_index()
else:
    filtered_data_dept = filtered_data_store[filtered_data_store['Dept'] == selected_dept]

# Gráfico de Linha: Vendas Médias por Departamento
fig_dept = go.Figure()
fig_dept.add_trace(go.Scatter(x=filtered_data_dept['Date'], y=filtered_data_dept['Weekly_Sales'], mode='lines', name='Vendas'))
fig_dept.add_trace(go.Scatter(x=filtered_data_dept['Date'], y=filtered_data_dept['Weekly_Sales'], mode='markers', name='Week', marker=dict(color='red', size=8)))
fig_dept.update_layout(title='Vendas Médias ao Longo do Tempo', xaxis_title='Data', yaxis_title='Vendas Semanais')
fig_dept.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

# Seção: Volume Médio de Vendas por Loja
fig_volume_vendas_loja = go.Figure()

if selected_store == 'Média Geral':
    fig_volume_vendas_loja = go.Figure(data=[go.Bar(x=avg_sales_per_store['Store'], y=avg_sales_per_store['Weekly_Sales'], name='Volume Medio de Vendas por Loja')])
else:
    fig_volume_vendas_loja = go.Figure(data=[go.Bar(x=[selected_store], y=[avg_sales_per_store[avg_sales_per_store['Store'] == selected_store]['Weekly_Sales'].iloc[0]], name='Volume Médio de Vendas por Loja')])

media_vendas = avg_sales_per_store['Weekly_Sales'].mean()
fig_volume_vendas_loja.add_hline(y=media_vendas, line_dash='dash', line_color='red', annotation_text=f'Média: {media_vendas:.2f}', annotation_position='bottom right', annotation_font_color='white')
fig_volume_vendas_loja.update_layout(title_text='Volume Médio de Vendas por Loja', xaxis_title='Numero da Loja', yaxis_title='Volume Médio de Vendas')
fig_volume_vendas_loja.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

# Organizando os gráficos em colunas
col1, col2 = st.columns(2)
with col1:
    if selected_dept != 'Média Geral' or selected_store != 'Média Geral':
        st.plotly_chart(fig_dept, use_container_width=True)
    else:
        avg_sales_per_store_department = df.groupby(['Date'])['Weekly_Sales'].mean().reset_index()
        fig_avg_sales_per_store_department = go.Figure()
        fig_avg_sales_per_store_department.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='lines', name='venda' ))
        fig_avg_sales_per_store_department.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='markers', name='Week', marker=dict(color='red', size=8)))
        fig_avg_sales_per_store_department.update_layout(title='Vendas Médias ao Longo do Tempo', xaxis_title='Data', yaxis_title='Vendas Semanais')
        fig_avg_sales_per_store_department.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
        st.plotly_chart(fig_avg_sales_per_store_department, use_container_width=True)

with col2:
    st.plotly_chart(fig_volume_vendas_loja, use_container_width=True)


#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

# Gráfico estilo px.scatter
fig_scatter = px.scatter(sorted_data, x='Weekly_Sales', y='Dept', color='Store', title='Lojas e Departamentos por Vendas Semanais', color_continuous_scale='blues')
st.plotly_chart(fig_scatter, use_container_width=True)


# Melhores lojas
Melhores_Lojas = avg_sales_per_store.loc[avg_sales_per_store['Weekly_Sales'] >= media_vendas]
Stores = Melhores_Lojas['Store'].unique()
Stores_info = df.loc[df['Store'].isin(Stores)]
avg_sales_per_store_department = Stores_info.groupby(['Store', 'Dept'])['Weekly_Sales'].mean().reset_index()

# Tabela: Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

st.title('Lojas que ficaram acima da média')
st.dataframe(sorted_data.reset_index(drop=True), width=1200)


