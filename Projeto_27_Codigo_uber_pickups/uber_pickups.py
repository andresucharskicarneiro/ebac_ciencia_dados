import streamlit as st
import pandas as pd
import numpy as np

# Título do aplicativo
st.title('Uber pickups em NOVA YORK - ASC')

# Definindo constante e URL dos dados
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Decorador para armazenar os dados em cache
@st.cache_data
def load_data(nrows):
    """Carrega um número específico de linhas de dados e armazena em cache."""
    # Carrega os dados do CSV
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # Renomeando colunas para minúsculas
    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    # Convertendo a coluna de data para o formato datetime
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Informe ao usuário que os dados estão sendo carregados
data_load_state = st.text('Carregando dados...')

# Carregue 10.000 linhas de dados no DataFrame
data = load_data(10000)

# Notifique que o carregamento foi concluído
data_load_state.text('Carregamento concluído! (usando st.cache_data)')

# Exibe uma amostra dos dados carregados
st.dataframe(data.head())

# Subtítulo para dados brutos
if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

# Subtítulo para o número de pickups por hora
st.subheader('Número de pickups por hora')

# Use NumPy para gerar um histograma que quebra os tempos de captação por hora
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

# Agora, vamos usar o método bar_chart do Streamlit para desenhar esse histograma
st.bar_chart(hist_values)

# Dica sobre bibliotecas de gráficos suportadas pelo Streamlit
st.markdown("""
É importante saber que o Streamlit suporta bibliotecas de gráficos mais complexas, como:
- Altair
- Bokeh
- Plotly
- Matplotlib
Para uma lista completa, veja as [bibliotecas de gráficos suportadas](https://docs.streamlit.io/library/api-reference/charts).
""")

# Exibindo um mapa de todas as pickups
st.subheader('Mapa de todas as pickups')
st.map(data)

# Filtrando pickups para uma hora específica
hour_to_filter = st.slider('Hora', 0, 23, 17)  # min: 0h, max: 23h, padrão: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Mapa de todas as pickups às {hour_to_filter}:00')
st.map(filtered_data)
