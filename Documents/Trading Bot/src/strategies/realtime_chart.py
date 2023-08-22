import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from binance.client import Client
from binance.enums import KLINE_INTERVAL_1MINUTE
import argparse

import os
import sys

# Obtén la ruta del directorio principal del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Agrega la ruta del directorio principal al sys.path
sys.path.append(project_root)

from data.data_processing import process_data

def get_realtime_data(pair, interval, limit):
    client = Client()

    # Obtener datos en tiempo real de Binance
    klines = client.get_klines(symbol=pair, interval=interval, limit=limit)

    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])

    # Convertir la columna 'timestamp' a tipo datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Convertir las columnas numéricas a tipo float
    numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                       'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_columns] = df[numeric_columns].astype(float)

    return df


def add_trading_markers(df, trades):
    # Agregar marcadores al gráfico para las órdenes de compra y venta
    for trade in trades:
        if trade['orden_compra'] == 'Buy':
            marker = '^'
            color = 'green'
        else:
            marker = 'v'
            color = 'red'

        plt.scatter(trade['fecha_compra'], trade['precio_compra'], marker=marker, color=color, s=100)
        plt.scatter(trade['fecha_venta'], trade['precio_venta'], marker=marker, color=color, s=100)

    plt.legend(['Buy', 'Sell'])


import datetime

# ... (código anterior) ...

def main(day=None):
    pair = 'BTCUSDT'
    interval = KLINE_INTERVAL_1MINUTE
    limit = 1000

    # Obtener los datos en tiempo real de Binance
    df = get_realtime_data(pair, interval, limit)

    # Convertir el índice a tipo DatetimeIndex
    df.set_index('timestamp', inplace=True)

    # Filtrar por el día especificado si se proporciona
    if day:
        df = df.loc[day]

    # Verificar si el DataFrame tiene datos
    if not df.empty:
        # Crear el gráfico de líneas en tiempo real
        mpf.plot(df, type='line', style='blueskies', title='Real-Time Chart', ylabel='Price', volume=True)

        # Obtener la fecha y la hora actuales
        now = datetime.datetime.now()
        date_text = now.strftime('%Y-%m-%d')
        time_text = now.strftime('%H:%M:%S')
        timezone_text = now.strftime('%Z')
        pair_text = f'Pair: {pair}'

        plt.text(0.05, 0.95, f'Date: {date_text}  Time: {time_text}  Timezone: {timezone_text}', transform=plt.gca().transAxes)
        plt.text(0.05, 0.90, pair_text, transform=plt.gca().transAxes)

        # Resto del código para implementar la estrategia de trading y agregar los marcadores al gráfico
        # ...
        # ...

        # Ejemplo de cómo agregar marcadores al gráfico
        trades = [
            {
                'fecha_compra': '2023-05-26 09:00:00',
                'precio_compra': 40000.0,
                'fecha_venta': '2023-05-26 10:00:00',
                'precio_venta': 42000.0,
                'orden_compra': 'Buy'
            },
            {
                'fecha_compra': '2023-05-26 11:00:00',
                'precio_compra': 43000.0,
                'fecha_venta': '2023-05-26 12:00:00',
                'precio_venta': 41000.0,
                'orden_compra': 'Sell'
            }
        ]

        add_trading_markers(df, trades)

        # Guardar el gráfico en un archivo
        plt.savefig('realtime_chart.png')
        print("Se ha guardado el gráfico en 'realtime_chart.png'. Por favor, ábrelo manualmente.")

    else:
        print("No se han obtenido datos en tiempo real. Verifica la conexión o inténtalo más tarde.")

main()

