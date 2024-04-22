import pandas as pd
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Carregar os dados
df = pd.read_csv('Output/Df_new.csv')

# Título do Dashboard
st.title('Análise de Vendas da Walmart')

# Criar o gráfico de linha
fig = go.Figure()

avg_sales_per_store_department = df.groupby(['Date'])['Weekly_Sales'].mean().reset_index()

fig.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='lines', name='Quantidade de Vendas da Semana'))
fig.add_trace(go.Scatter(x=avg_sales_per_store_department['Date'], y=avg_sales_per_store_department['Weekly_Sales'], mode='markers', name='Semana', marker=dict(color='red', size=8)))

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Média do Volume de Vendas Semanais ao Longo do Tempo',
                   xaxis_title='Data',
                   yaxis_title='Vendas Semanais')

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=30,
                     label="1M",
                     step="day",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)


# Criar o gráfico de barra
fig = go.Figure()

avg_sales_per_store = df.groupby(['Store'])['Weekly_Sales'].mean().reset_index()

# Use o argumento hovertext para o texto de hover
fig = go.Figure(data=[go.Bar(x=avg_sales_per_store['Store'], y=avg_sales_per_store['Weekly_Sales'], name='Volume Médio de Vendas por Loja')])

media_vendas = avg_sales_per_store['Weekly_Sales'].mean()
fig.add_hline(y=media_vendas, line_dash='dash', line_color='red', annotation_text=f'Média: {media_vendas:.2f}', annotation_position='bottom right')

fig.update_layout(title_text='Volume Médio de Vendas por Loja', xaxis_title='Número da Loja', yaxis_title='Volume Médio de Vendas')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

Melhores_Lojas = avg_sales_per_store.loc[avg_sales_per_store['Weekly_Sales']>= media_vendas]

# Criar o gráfico de tabela
fig = go.Figure(data=[go.Table(
    header=dict(values=list(Melhores_Lojas.columns),  
                align='left'),
    cells=dict(values=[Melhores_Lojas['Store'], Melhores_Lojas['Weekly_Sales']],
               align='left'))
])

# Definir os botões de seleção para ordenar as lojas
dropdown_buttons = [
    dict(label='Menor para Maior',
         method='restyle',
         args=[{'cells.values[0]': [Melhores_Lojas['Store'].iloc[Melhores_Lojas['Weekly_Sales'].argsort()]],
                'cells.values[1]': [Melhores_Lojas['Weekly_Sales'].sort_values()]}]),
    dict(label='Maior para Menor',
         method='restyle',
         args=[{'cells.values[0]': [Melhores_Lojas['Store'].iloc[Melhores_Lojas['Weekly_Sales'].argsort()[::-1]]],
                'cells.values[1]': [Melhores_Lojas['Weekly_Sales'].sort_values(ascending=False)]}])
]

# Adicionar botões de seleção ao layout
fig.update_layout(
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.87,
            xanchor='left',
            y=1.2,
            yanchor='top'
        ),
    ]
)

# Adicionar título e rótulos dos eixos
fig.update_layout(title_text='Lojas com Maior Volume Médio de Vendas', xaxis_title='Número da Loja',
                   yaxis_title='Volume Médio de Vendas')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

Stores = Melhores_Lojas['Store'].unique()

Stores_info = df.loc[df['Store'].isin(Stores)]

avg_sales_per_store_department = Stores_info.groupby(['Store','Dept'])['Weekly_Sales'].mean().reset_index()

# Obtendo lojas únicas
lojas_unicas = avg_sales_per_store_department['Store'].unique()

# Criar o gráfico de tabela
fig = go.Figure(data=[go.Table(
    header=dict(values=list(avg_sales_per_store_department.columns),  
                align='left'),
    cells=dict(values=[avg_sales_per_store_department['Store'], avg_sales_per_store_department['Dept'], avg_sales_per_store_department['Weekly_Sales']],
               align='left'))
])

# Definir os botões de seleção para ordenar as lojas
dropdown_buttons = [
    dict(label='Menor para Maior',
         method='restyle',
         args=[{'cells.values[0]': [avg_sales_per_store_department['Store'].iloc[avg_sales_per_store_department['Weekly_Sales'].argsort()]],
                'cells.values[1]': [avg_sales_per_store_department['Dept'].iloc[avg_sales_per_store_department['Weekly_Sales'].argsort()]],
                'cells.values[2]': [avg_sales_per_store_department['Weekly_Sales'].sort_values()]}]),
    dict(label='Maior para Menor',
         method='restyle',
         args=[{'cells.values[0]': [avg_sales_per_store_department['Store'].iloc[avg_sales_per_store_department['Weekly_Sales'].argsort()[::-1]]],
                'cells.values[1]': [avg_sales_per_store_department['Dept'].iloc[avg_sales_per_store_department['Weekly_Sales'].argsort()[::-1]]],
                'cells.values[2]': [avg_sales_per_store_department['Weekly_Sales'].sort_values(ascending=False)]}])
]

# Adicionar botões de seleção ao layout
fig.update_layout(
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.87,
            xanchor='left',
            y=1.2,
            yanchor='top'
        ),
        
    ]
)

# Adicionar título e rótulos dos eixos
fig.update_layout(title_text='Vendas Semanais Médias por Loja e Departamento',
                   xaxis_title='Loja',
                   yaxis_title='Departamento')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criando o gráfico de dispersão
fig = px.scatter(avg_sales_per_store_department, 
                 y=avg_sales_per_store_department['Weekly_Sales'], 
                 x=avg_sales_per_store_department['Store'], 
                 color='Weekly_Sales',
                 hover_name='Dept',
                 labels={'Weekly_Sales': 'Vendas Semanais', 'Dept': 'Departamento', 'Store': 'Loja'})

# Adicionando a linha da média
media_vendas = avg_sales_per_store_department['Weekly_Sales'].mean()
fig.add_hline(y=media_vendas, line_dash='dash', line_color='red', annotation_text=f'Média: {media_vendas:.2f}', annotation_position='bottom right')

# Adicionando título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias por Loja e Departamento',
                  xaxis_title='Loja',
                  yaxis_title='Vendas Semanais')

# Mostrando o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=False)

avg_sales_per_holiday = df.groupby(['IsHoliday'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de barras
fig = go.Figure(data=[go.Bar(x=avg_sales_per_holiday['IsHoliday'], y=avg_sales_per_holiday['Weekly_Sales'])])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias em Feriados',
                   xaxis_title='Feriado',
                   yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

df_holiday = df.loc[df['IsHoliday']==True]

super_bowl_dates = ["2010-02-12", "2011-02-11", "2012-02-10"]
df['SuperBowl'] = df['Date'].isin(super_bowl_dates)

Labor_day_dates = ["2010-09-10", "2011-10-09", "2012-02-07"]
df['LaborDay'] = df['Date'].isin(Labor_day_dates)

Thanksgiving_dates = ["2010-11-26", "2011-11-25", "2012-11-23"]
df['Thanksgiving'] = df['Date'].isin(Thanksgiving_dates)

Christmas_dates = ["2010-12-31", "2011-12-30", "2012-12-28"]
df['Christmas'] = df['Date'].isin(Christmas_dates)

avg_sales_per_SuperBowl = df.groupby(['SuperBowl'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_LaborDay = df.groupby(['LaborDay'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_Thanksgiving = df.groupby(['Thanksgiving'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_Christmas = df.groupby(['Christmas'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de barras
fig = go.Figure(data=[go.Bar(x=avg_sales_per_SuperBowl['SuperBowl'], y=avg_sales_per_SuperBowl['Weekly_Sales'])])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias no Super Bowl',
                   xaxis_title='Super Bowl',
                   yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de barras
fig = go.Figure(data=[go.Bar(x=avg_sales_per_LaborDay['LaborDay'], y=avg_sales_per_LaborDay['Weekly_Sales'])])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias no Dia do Trabalho',
                   xaxis_title='Dia do Trabalho',
                   yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de barras
fig = go.Figure(data=[go.Bar(x=avg_sales_per_Thanksgiving['Thanksgiving'], y=avg_sales_per_Thanksgiving['Weekly_Sales'])])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias no Dia de Ação de Graças',
                   xaxis_title='Dia de Ação de Graças',
                   yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de barras
fig = go.Figure(data=[go.Bar(x=avg_sales_per_Christmas['Christmas'], y=avg_sales_per_Christmas['Weekly_Sales'])])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias no Natal',
                   xaxis_title='Natal',
                   yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)


avg_sales_per_type_superbowl = df.groupby(['Type','SuperBowl'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_type_laborday = df.groupby(['Type','LaborDay'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_type_thanksgiving = df.groupby(['Type','Thanksgiving'])['Weekly_Sales'].mean().reset_index()
avg_sales_per_type_christman = df.groupby(['Type','Christmas'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de dispersão
fig = px.scatter(avg_sales_per_type_superbowl, x=avg_sales_per_type_superbowl['Type'], y=avg_sales_per_type_superbowl['Weekly_Sales'], color=avg_sales_per_type_superbowl['SuperBowl'])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias por Tipo e Super Bowl',
                  xaxis_title='Tipo',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de dispersão
fig = px.scatter(avg_sales_per_type_laborday, x=avg_sales_per_type_laborday['Type'], y=avg_sales_per_type_laborday['Weekly_Sales'], color=avg_sales_per_type_laborday['LaborDay'])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias por Tipo e Dia do Trabalho',
                  xaxis_title='Tipo',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de dispersão
fig = px.scatter(avg_sales_per_type_thanksgiving, x=avg_sales_per_type_thanksgiving['Type'], y=avg_sales_per_type_thanksgiving['Weekly_Sales'], color=avg_sales_per_type_thanksgiving['Thanksgiving'])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias por Tipo e Dia de Ação de Graças',
                  xaxis_title='Tipo',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

# Criar o gráfico de dispersão
fig = px.scatter(avg_sales_per_type_christman, x=avg_sales_per_type_christman['Type'], y=avg_sales_per_type_christman['Weekly_Sales'], color=avg_sales_per_type_christman['Christmas'])

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias por Tipo e Natal',
                  xaxis_title='Tipo',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=False)

avg_sales_per_type = df.groupby(['Type'])['Weekly_Sales'].mean().reset_index()

Total_sum = avg_sales_per_type['Weekly_Sales'].sum()

# Calculate the percentage of each store type
store_type_percentage = (avg_sales_per_type['Weekly_Sales'] / Total_sum) * 100

labels = ['A','B','C']

# Criar o gráfico de pizza
fig = px.pie(store_type_percentage, values=store_type_percentage, names=labels, title='Porcentagem de vendas de cada tipo de loja')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)

df["Date"] = pd.to_datetime(df["Date"])  # convert to datetime
df['week'] = df['Date'].dt.isocalendar().week
df['month'] = df['Date'].dt.month 
df['year'] = df['Date'].dt.year

avg_sales_per_week = df.groupby(['week','year'])['Weekly_Sales'].mean().reset_index()

avg_sales_per_month = df.groupby(['month','year'])['Weekly_Sales'].mean().reset_index()

avg_sales_per_year = df.groupby(['year'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de linha
fig = px.line(avg_sales_per_week, x=avg_sales_per_week['week'], y=avg_sales_per_week['Weekly_Sales'], text=avg_sales_per_week['week'], color=avg_sales_per_week['year'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias ao Longo do Tempo',
                  xaxis_title='Semana',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)

# Criar o gráfico de linha
fig = px.line(avg_sales_per_month, x=avg_sales_per_month['month'], y=avg_sales_per_month['Weekly_Sales'], text=avg_sales_per_month['month'], color=avg_sales_per_month['year'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Mensais Médias ao Longo do Tempo',
                  xaxis_title='Mês',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)

avg_sales_per_fuelprice = df.groupby(['Fuel_Price'])['Weekly_Sales'].mean().reset_index()

avg_sales_per_cpi = df.groupby(['CPI'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de linha
fig = px.line(avg_sales_per_fuelprice, x=avg_sales_per_fuelprice['Fuel_Price'], y=avg_sales_per_fuelprice['Weekly_Sales'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias em relação ao Preço do Combustível',
                  xaxis_title='Preço do Combustível',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)

# Criar o gráfico de linha
fig = px.line(avg_sales_per_cpi, x=avg_sales_per_cpi['CPI'], y=avg_sales_per_cpi['Weekly_Sales'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias em relação ao Índice de Preços ao Consumidor (CPI)',
                  xaxis_title='Índice de Preços ao Consumidor (CPI)',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)

avg_sales_per_Unemployment = df.groupby(['Unemployment'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de linha
fig = px.line(avg_sales_per_Unemployment, x=avg_sales_per_Unemployment['Unemployment'], y=avg_sales_per_Unemployment['Weekly_Sales'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias em relação à Taxa de Desemprego',
                  xaxis_title='Taxa de Desemprego',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)


avg_sales_per_temp = df.groupby(['Temperature'])['Weekly_Sales'].mean().reset_index()

# Criar o gráfico de linha
fig = px.line(avg_sales_per_Unemployment, x=avg_sales_per_Unemployment['Unemployment'], y=avg_sales_per_Unemployment['Weekly_Sales'])
fig.update_traces(textposition="bottom right")

# Adicionar título e rótulos dos eixos
fig.update_layout(title='Vendas Semanais Médias em relação à Taxa de Desemprego',
                  xaxis_title='Taxa de Desemprego',
                  yaxis_title='Vendas Semanais')

# Mostrar o gráfico no Streamlit com o tamanho da página inteira
st.plotly_chart(fig, use_container_width=True)
