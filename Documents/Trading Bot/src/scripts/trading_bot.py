import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.append("C:/Users/durot/Documents/Trading Bot/src")
from data.binance_client import client
from data.data_processing import process_data
from strategies.trading_strategy import implement_trading_strategy

# Parámetros de las Bandas de Bollinger
length = 15
mult = 2.5

# Parámetros del RSI
rsilen = 10
rsiob = 80
rsios = 20

# Lista de pares de criptomonedas para simular el trading
pairs = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

# Obtén la fecha y hora actuales
end_time = datetime.now()
start_time = end_time - timedelta(days=7)

# Convierte las fechas a formato UNIX timestamp
start_time = int(start_time.timestamp()) * 1000
end_time = int(end_time.timestamp()) * 1000

profits = []
invested_amount = 0

# Itera sobre los pares de criptomonedas
for pair in pairs:
    # Obtén los datos procesados
    df = process_data(pair, start_time, end_time, length, mult, rsilen, rsios, rsiob)
    
    # Implementa la estrategia de trading
    pair_profits, pair_wallet_balance = implement_trading_strategy(pair, start_time, end_time, length, mult, rsilen, rsios, rsiob)
    
    # Verifica si se generaron transacciones exitosas
    if pair_profits:
        profits.extend(pair_profits)
        invested_amount += pair_wallet_balance

# Imprime los datos generados en profits
print("Datos generados en profits:")
print(profits)

# Crea una lista de diccionarios a partir de los datos en profits
data = []
for row in profits:
    if isinstance(row, dict):  # Verifica que el elemento sea un diccionario
        data.append(row)

# Imprime los datos generados en data
print("Datos generados en data:")
print(data)

# Crea un DataFrame a partir de la lista de diccionarios
df = pd.DataFrame(data)

# Crea la carpeta si no existe
output_dir = 'src/backtesting_files'
os.makedirs(output_dir, exist_ok=True)

# Guarda el DataFrame en un archivo de Excel
file_path = os.path.join(output_dir, 'registro_trading.xlsx')
df.to_excel(file_path, index=False)
print("Archivo de Excel guardado en:", file_path)
