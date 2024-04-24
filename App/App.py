import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


# Carregar os dados

df = pd.read_csv("Output/Df_new.csv")
df["Date"] = pd.to_datetime(df["Date"])  # convert to datetime
df['Week'] = df['Date'].dt.isocalendar().week
df['Month'] = df['Date'].dt.month 
df['Year'] = df['Date'].dt.year

avg_sales_per_store_department = df.groupby(['Date', 'Store', 'Dept','Week','Year','Month'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store = df.groupby(['Store'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department['Date'] = pd.to_datetime(avg_sales_per_store_department['Date'])

# Configurações
colors = {
    'background': '#0f1116',
    'text': '#17202A',
    'plot_color': '#5499C7',
    'section_title': '#1F618D',
    'highlight': '#E74C3C',
    'button_color': '#1ABC9C'
}


st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state='collapsed',
    )


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
    filtered_data_dept = filtered_data_store.groupby(['Date','Week','Year','Month'])['Weekly_Sales'].mean().reset_index()
else:
    filtered_data_dept = filtered_data_store[filtered_data_store['Dept'] == selected_dept]

# Gráfico de Linha: Vendas Médias por Departamento
fig_dept = go.Figure()
fig_dept.add_trace(go.Scatter(x=filtered_data_dept['Date'], y=filtered_data_dept['Weekly_Sales'], mode='lines', name='Vendas'))
fig_dept.add_trace(go.Scatter(x=filtered_data_dept['Date'], y=filtered_data_dept['Weekly_Sales'], mode='markers', name='Week', marker=dict(color='red', size=8)))
fig_dept.update_layout(title='Vendas Médias ao Longo do Tempo', xaxis_title='Data', yaxis_title='Vendas Semanais')
# fig_dept.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

fig_time_week = px.line(filtered_data_dept, x='Week', y='Weekly_Sales', text='Week', color='Year')
fig_time_week.update_traces(textposition="bottom right")

fig_time_month = px.line(filtered_data_dept, x='Month', y='Weekly_Sales', text='Month', color='Year')
fig_time_month.update_traces(textposition="bottom right")

# Seção: Volume Médio de Vendas por Loja
fig_volume_vendas_loja = go.Figure()

if selected_store == 'Média Geral':
    fig_volume_vendas_loja = go.Figure(data=[go.Bar(x=avg_sales_per_store['Store'], y=avg_sales_per_store['Weekly_Sales'], name='Volume Medio de Vendas por Loja')])
else:
    fig_volume_vendas_loja = go.Figure(data=[go.Bar(x=[selected_store], y=[avg_sales_per_store[avg_sales_per_store['Store'] == selected_store]['Weekly_Sales'].iloc[0]], name='Volume Médio de Vendas por Loja')])

media_vendas = avg_sales_per_store['Weekly_Sales'].mean()
fig_volume_vendas_loja.add_hline(y=media_vendas, line_dash='dash', line_color='red', annotation_text=f'Média: {media_vendas:.2f}', annotation_position='bottom right', annotation_font_color='black')
fig_volume_vendas_loja.update_layout(title_text='Volume Médio de Vendas por Loja', xaxis_title='Numero da Loja', yaxis_title='Volume Médio de Vendas')
# fig_volume_vendas_loja.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])


# Organizando os gráficos em colunas
col1, col2 = st.columns(2, gap='medium')
with col1:
    if selected_dept != 'Média Geral' or selected_store != 'Média Geral':
        st.plotly_chart(fig_dept, use_container_width=True)
        st.plotly_chart(fig_time_week, use_container_width=True)
    else:
        avg_sales_per_store_department = df.groupby(['Date'])['Weekly_Sales'].mean().reset_index()
        fig_avg_sales_per_store_department = go.Figure()
        fig_avg_sales_per_store_department.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='lines', name='venda' ))
        fig_avg_sales_per_store_department.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='markers', name='Week', marker=dict(color='red', size=8)))
        fig_avg_sales_per_store_department.update_layout(title='Vendas Médias ao Longo do Tempo', xaxis_title='Data', yaxis_title='Vendas Semanais')
        # fig_avg_sales_per_store_department.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
        st.plotly_chart(fig_avg_sales_per_store_department, use_container_width=True)
        avg_sales_per_week = df.groupby(['Week','Year'])['Weekly_Sales'].mean().reset_index()
        fig_time_week = px.line(avg_sales_per_week, x=avg_sales_per_week['Week'], y=avg_sales_per_week['Weekly_Sales'], text=avg_sales_per_week['Week'], color=avg_sales_per_week['Year'])
        fig_time_week.update_traces(textposition="bottom right")
        fig_time_week.update_layout(title='Vendas Médias ao Longo das Semanas', xaxis_title='Semana', yaxis_title='Vendas Semanais')
        st.plotly_chart(fig_time_week, use_container_width=True)

with col2:
    st.plotly_chart(fig_volume_vendas_loja, use_container_width=True)
    if selected_dept != 'Média Geral' or selected_store != 'Média Geral':
        fig_time_month = px.line(filtered_data_dept, x='Month', y='Weekly_Sales', text='Month', color='Year')
        fig_time_month.update_traces(textposition="bottom right")
        fig_time_month.update_layout(title='Vendas Médias ao Longo dos Meses', xaxis_title='Mês', yaxis_title='Vendas Semanais')
        st.plotly_chart(fig_time_month, use_container_width=True)
    else:
        avg_sales_per_month = df.groupby(['Month','Year'])['Weekly_Sales'].mean().reset_index()
        fig_time_month = px.line(avg_sales_per_month, x=avg_sales_per_month['Month'], y=avg_sales_per_month['Weekly_Sales'], text=avg_sales_per_month['Month'], color=avg_sales_per_month['Year'])
        fig_time_month.update_traces(textposition="bottom right")
        fig_time_month.update_layout(title='Vendas Médias ao Longo dos Meses', xaxis_title='Mês', yaxis_title='Vendas Semanais')
        st.plotly_chart(fig_time_month, use_container_width=True)
    



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
fig_scatter.update_layout(xaxis_title='Vendas Semanais', yaxis_title='Departamento')
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
st.dataframe(sorted_data.reset_index(drop=True), use_container_width=True)



#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','IsHoliday'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['IsHoliday'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]


st.title('Análise da influência dos feriados nas vendas')
col1, col2 = st.columns(2)
# Gráfico estilo px.scatter
with col1:
    fig_scatter = px.bar(sorted_data, x='IsHoliday', y='Weekly_Sales', color='Store', title='Lojas e Departamentos por Vendas Semanais nos Feriados', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Feriado', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_scatter = px.bar(avg_sales_per_store_department1, x='IsHoliday', y='Weekly_Sales', title='Vendas Semanais nos Feriados', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Feriado', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)


df_holiday = df.loc[df['IsHoliday']==True]
df_not_holiday = df.loc[df['IsHoliday']==False]

super_bowl_dates = ["2010-02-12", "2011-02-11", "2012-02-10"]
df['SuperBowl'] = df['Date'].isin(super_bowl_dates)
Labor_day_dates = ["2010-09-10", "2011-10-09", "2012-02-07"]
df['LaborDay'] = df['Date'].isin(Labor_day_dates)
Thanksgiving_dates = ["2010-11-26", "2011-11-25", "2012-11-23"]
df['Thanksgiving'] = df['Date'].isin(Thanksgiving_dates)
Christmas_dates = ["2010-12-31", "2011-12-30", "2012-12-28"]
df['Christmas'] = df['Date'].isin(Christmas_dates)


#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','SuperBowl'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['SuperBowl'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.bar(sorted_data, x='SuperBowl', y='Weekly_Sales', title='Lojas e Departamentos por Vendas Semanais no SuperBowl', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='SuperBowl', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)
with col2:
    fig_scatter = px.bar(avg_sales_per_store_department1, x='SuperBowl', y='Weekly_Sales', title='Vendas Semanais no SuperBowl', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='SuperBowl', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','LaborDay'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['LaborDay'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.bar(sorted_data, x='LaborDay', y='Weekly_Sales', title='Lojas e Departamentos por Vendas Semanais no LaborDay', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='LaborDay', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)
with col2:
    fig_scatter = px.bar(avg_sales_per_store_department1, x='LaborDay', y='Weekly_Sales', title='Vendas Semanais no LaborDay', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='LaborDay', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Thanksgiving'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Thanksgiving'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.bar(sorted_data, x='Thanksgiving', y='Weekly_Sales', title='Lojas e Departamentos por Vendas Semanais no Thanksgiving', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Thanksgiving', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)
with col2:
    fig_scatter = px.bar(avg_sales_per_store_department1, x='Thanksgiving', y='Weekly_Sales', title='Vendas Semanais no Thanksgiving', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Thanksgiving', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Christmas'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Christmas'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.bar(sorted_data, x='Christmas', y='Weekly_Sales', title='Lojas e Departamentos por Vendas Semanais no Christmas', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Christmas', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)
with col2:
    fig_scatter = px.bar(avg_sales_per_store_department1, x='Christmas', y='Weekly_Sales', title='Vendas Semanais no Christmas', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Christmas', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)










st.title('Análise da influência dos feriados nas vendas nos tipo de lojas')

#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Type','SuperBowl',])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Type','SuperBowl'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.scatter(sorted_data, x='Type', y='Weekly_Sales',color='SuperBowl', title='Lojas e Departamentos por Vendas Semanais no SuperBowl', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)


with col2:
    fig_scatter = px.scatter(avg_sales_per_store_department1, x='Type', y='Weekly_Sales', color='SuperBowl', title='Vendas Semanais no SuperBowl', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)



#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Type','LaborDay',])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Type','LaborDay'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.scatter(sorted_data, x='Type', y='Weekly_Sales',color='LaborDay', title='Lojas e Departamentos por Vendas Semanais no LaborDay', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)


with col2:
    fig_scatter = px.scatter(avg_sales_per_store_department1, x='Type', y='Weekly_Sales', color='LaborDay', title='Vendas Semanais no LaborDay', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)





#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Type','Thanksgiving',])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Type','Thanksgiving'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.scatter(sorted_data, x='Type', y='Weekly_Sales',color='Thanksgiving', title='Lojas e Departamentos por Vendas Semanais no Thanksgiving', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_scatter = px.scatter(avg_sales_per_store_department1, x='Type', y='Weekly_Sales', color='Thanksgiving', title='Vendas Semanais no Thanksgiving', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)



#lojas
avg_sales_per_store_department = df.groupby(['Store', 'Dept','Type','Christmas',])['Weekly_Sales'].mean().reset_index()
avg_sales_per_store_department1 = df.groupby(['Type','Christmas'])['Weekly_Sales'].mean().reset_index()

# Melhores lojas, departamentos e vendas semanais por departamento
sorted_data = avg_sales_per_store_department.sort_values(by='Weekly_Sales', ascending=False)

if selected_store != 'Média Geral' and selected_dept != 'Média Geral':
    sorted_data = sorted_data[(sorted_data['Store'] == selected_store) & (sorted_data['Dept'] == selected_dept)]
elif selected_store != 'Média Geral':
    sorted_data = sorted_data[sorted_data['Store'] == selected_store]

col1, col2 = st.columns(2)
with col1:
    fig_scatter = px.scatter(sorted_data, x='Type', y='Weekly_Sales',color='Christmas', title='Lojas e Departamentos por Vendas Semanais no Christmas', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_scatter = px.scatter(avg_sales_per_store_department1, x='Type', y='Weekly_Sales', color='Christmas', title='Vendas Semanais no Christmas', color_continuous_scale='blues')
    fig_scatter.update_layout(xaxis_title='Tipo de Loja', yaxis_title='Vendas Semanais')
    st.plotly_chart(fig_scatter, use_container_width=True)


avg_sales_per_type = df.groupby(['Type'])['Weekly_Sales'].mean().reset_index()
Total_sum = avg_sales_per_type['Weekly_Sales'].sum()
store_type_percentage = (avg_sales_per_type['Weekly_Sales'] / Total_sum) * 100
labels = ['A','B','C']

fig = px.pie(store_type_percentage, values = store_type_percentage, names = labels, title='Porcentagem de vendas de cada tipo de loja')
st.plotly_chart(fig, use_container_width=True)


st.title('Análise da influência de Temperatura, Gasolina, Desemprego e Temperatura nas vendas')

avg_sales_per_fuelprice = df.groupby(['Fuel_Price'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_cpi = df.groupby(['CPI'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_Unemployment = df.groupby(['Unemployment'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_temp = df.groupby(['Temperature'])['Weekly_Sales'].mean().reset_index()

col1, col2 = st.columns(2)
with col1:
    fig = px.line(avg_sales_per_fuelprice, x=avg_sales_per_fuelprice['Fuel_Price'], y=avg_sales_per_fuelprice['Weekly_Sales'])
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(avg_sales_per_cpi, x=avg_sales_per_cpi['CPI'], y=avg_sales_per_cpi['Weekly_Sales'])
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig, use_container_width=True)


with col2:
    fig = px.line(avg_sales_per_Unemployment, x=avg_sales_per_Unemployment['Unemployment'], y=avg_sales_per_Unemployment['Weekly_Sales'])
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(avg_sales_per_temp, x=avg_sales_per_temp['Temperature'], y=avg_sales_per_temp['Weekly_Sales'])
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig, use_container_width=True)