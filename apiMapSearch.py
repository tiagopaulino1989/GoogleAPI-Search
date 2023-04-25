#!pip install googlemaps

import pandas as pd
import googlemaps
from datetime import datetime
from tqdm import tqdm
import time

tqdm.pandas()

# Chave de API Google Maps
GMAPS_API_KEY = ''
# Nome do campo que contém o "adress" no DataFrame
ADRESS_FEATURE= 'endereço'

# Ler o arquivo com os endereços
df = pd.read_excel('.xlsx')

# Inicializar o objeto Google Maps
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Função para obter a localização (latitude e longitude) de um endereço
def get_location(address):
    geocode_result = gmaps.geocode(address)
    # time.sleep(0.05)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return pd.Series({'latitude': lat, 'longitude': lng})
    else:
        return pd.Series({'latitude': None, 'longitude': None})

# Aplicar a função em cada linha do DataFrame com uma barra de progresso
df[['latitude', 'longitude']] = df[ADRESS_FEATURE].progress_apply(get_location)

# Exportar o dataframe para um arquivo Excel
df.to_excel('arquivo_com_lat_lon.xlsx', index=False)