import yfinance as yf
import csv
import pandas as pd
import copy
import pandas_ta as ta


def fetch_stock_data(ticker, period='1mo'):
    """
    Получает исторические данные об акциях для указанного тикера и временного периода.
    Возвращает DataFrame с данными.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """Вычисляет и выводит среднюю цену закрытия акций за заданный период."""
    data_avr = data['Close'].mean()
    return data_avr


def notify_if_strong_fluctuations(data, threshold):
    """
    Вычисляет максимальное и минимальное значения цены закрытия и сравнивает разницу с заданным порогом.
    Если разница превышает порог, пользователь получает уведомление.
    """
    data_close = data['Close']

    close_max = max(data_close)
    close_min = min(data_close)

    volatility = (close_max - close_min) / close_min * 100
    if volatility > threshold:
        print(f'Внимание. Волатильность {volatility:.1f}% для данного инструмента превысила порог в {threshold:.1f}%')


def export_data_to_csv(data, filename):
    """Позволяет сохранять загруженные данные об акциях в CSV файл"""
    with open(filename, 'w', newline='') as out_csv:
        writer = csv.writer(out_csv, delimiter=',')
        df = pd.DataFrame(data)
        df.to_csv(filename)


def calculate_rsi(data):
    """Вычисляет и выводит значения индикатора RSI cо стандартным периодом 14."""
    df = copy.copy(data)

    # Calculate RSI values using the pandas_ta library
    df['RSI'] = df.ta.rsi(close='close', length=14)
    return df


def calculate_macd(data):
    """
    Вычисляет и выводит значения индикатора MACD за заданный период.
    Стандартные настройки:
    ЕМАs — (короткая) с периодом 12 дней (две недели).
    ЕМАl — (длинная) с периодом 26 дней (месяц).
    EМАa — (сглаживающая разницу) с периодом 9 значений.
    """
    df = copy.copy(data)

    df = df[['Close', 'Open', 'High', 'Volume', 'Low']]
    data = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

    return data
