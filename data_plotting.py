import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создаёт график, отображающий цены закрытия и скользящие средние.
    Предоставляет возможность сохранения графика в файл.
    """
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def plot_rsi(data, ticker):
    """
    Создаёт и показывает график, отображающий индикатор RSI.
    """

    plt.figure(figsize=(10, 6))

    if 'Date' in data:
        dates = data['Date']
    else:
        dates = data.index.to_numpy()

    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dates, data['Close'], label='Close Price')
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel('Цена акции')
    plt.legend()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    x_min = dates[0]
    x_max = dates[-1]
    plt.plot(dates, data['RSI'], label='RSI', color='red')
    plt.hlines(70, x_min, x_max, colors='g', linestyles='dotted')
    plt.hlines(30, x_min, x_max, colors='g', linestyles='dotted')
    plt.title(f"Relative Strength Index (RSI) индикатор для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def plot_macd(data, ticker):
    """
    Создаёт и показывает график, отображающий индикатор MACD.
    """
    plt.figure(figsize=(10, 6))

    if 'Date' in data:
        dates = data['Date']
    else:
        dates = data.index.to_numpy()

    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dates, data['MACD_12_26_9'], label='MA 12', color='red')
    plt.plot(dates, data['MACDh_12_26_9'], label='MA 26')
    plt.title(f"Moving Average Convergence-Divergence (MACD) индикатор для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("MA")
    plt.legend()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    x_min = dates[0]
    x_max = dates[-1]
    plt.plot(dates, data['MACDs_12_26_9'], label='Signal', color='green')
    plt.hlines(0, x_min, x_max, colors='r', linestyles='dotted')
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    plt.subplots_adjust(hspace=0.5)
    plt.show()
