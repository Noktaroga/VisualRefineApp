import numpy as np
from data.data_processing import process_data

def implement_trading_strategy(pair, start_time, end_time, length, mult, rsilen, rsios, rsiob):
    df = process_data(pair, start_time, end_time, length, mult, rsilen, rsios, rsiob)

    position = 0
    buy_price = 0
    take_profit_percent = 0.01  # 1.0%
    stop_loss_percent = 0.01  # 1.0%
    wallet_balance = 10
    invested_amount = wallet_balance  # Inicialmente igual al saldo del monedero
    profits = []

    for index, row in df.iterrows():
        if row['buy_signal']:
            if position == 0:
                # Abre una posición de compra
                buy_price = row['close']
                stop_loss = buy_price * (1 - stop_loss_percent)
                take_profit = buy_price * (1 + take_profit_percent)
                position = 1
                invested_amount -= invested_amount * stop_loss_percent  # Decrementa la inversión por la posible pérdida
                buy_date = index.strftime('%Y-%m-%d %H:%M:%S')
                print("¡Se ha abierto una posición de compra!")

                # Crea un diccionario con los datos de la transacción exitosa
                transaction = {
                    'pair': row['pair'],
                    'fecha_compra': buy_date,
                    'precio_compra': buy_price,
                    'fecha_venta': None,
                    'precio_venta': None,
                    'orden_compra': 'Buy',
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'inversion': invested_amount,
                    'ganancia_perdida': 0
                }
                profits.append(transaction)
            else:
                print("Ya hay una orden de compra abierta. No se puede abrir una nueva orden.")

        elif row['sell_signal']:
            if position == 1:
                # Cierra la posición de compra
                sell_price = row['close']
                position = 0
                sell_date = index.strftime('%Y-%m-%d %H:%M:%S')

                if sell_price >= take_profit:
                    order_type = 'Take Profit'
                    gain_loss = invested_amount * take_profit_percent
                    sell_price = take_profit  # Asocia el precio de venta con el take profit
                else:
                    order_type = 'Stop Loss'
                    gain_loss = invested_amount * stop_loss_percent
                    sell_price = stop_loss  # Asocia el precio de venta con el stop loss

                wallet_balance += gain_loss
                transaction = profits[-1]
                transaction['fecha_venta'] = sell_date
                transaction['precio_venta'] = sell_price
                transaction['orden_compra'] = order_type
                transaction['ganancia_perdida'] = gain_loss

                invested_amount -= invested_amount * stop_loss_percent  # Decrementa la inversión por la pérdida

                print("¡Se ha cerrado una posición de compra!")

            elif position == 1 and profits[-1]['orden_compra'] == 'Buy':
                print("¡La orden de compra anterior sigue abierta!")
                continue

    return profits, wallet_balance
