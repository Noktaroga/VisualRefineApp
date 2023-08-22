import pandas as pd
import ta
from binance.client import Client
from data.binance_client import api_key, api_secret
import pytz

def get_historical_data(pair, start_time, end_time):
    # Obtén los datos históricos utilizando la API de Binance
    client = Client(api_key, api_secret)
    interval = Client.KLINE_INTERVAL_1MINUTE
    klines = client.get_historical_klines(pair, interval, start_time, end_time)

    # Procesa los datos históricos en un DataFrame de pandas
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades_count', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Ajusta la zona horaria de los datos a UTC-4
    timezone = pytz.timezone('Etc/GMT+4')
    df['timestamp'] = df['timestamp'].dt.tz_localize(pytz.UTC).dt.tz_convert(timezone)
    df['timestamp'] = df['timestamp'].dt.tz_convert(None)

    df.set_index('timestamp', inplace=True)
    df = df.astype(float)

    return df

def process_data(pair, start_time, end_time, length, mult, rsilen, rsios, rsiob):
    # Obtén los datos históricos
    df = get_historical_data(pair, start_time, end_time)

    # Calcula las Bandas de Bollinger
    df['basis'] = df['close'].rolling(window=length).mean()
    df['std'] = df['close'].rolling(window=length).std()
    df['upper'] = df['basis'] + (df['std'] * mult)
    df['lower'] = df['basis'] - (df['std'] * mult)

    # Calcula el RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=rsilen)
    df['pair'] = pair

    # Genera la columna 'buy_signal' basada en tus condiciones de compra
    df['buy_signal'] = (df['rsi'] < rsiob) & (df['rsi'].shift(1) >= rsiob)

    # Genera la columna 'sell_signal' basada en tus condiciones de venta
    df['sell_signal'] = (df['rsi'] > rsios) & (df['rsi'].shift(1) <= rsios)

    df['orden_compra'] = None

    return df
