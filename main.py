import data_download as dd
import data_plotting as dplt
from datetime import datetime  # для генерирования имени csv файла


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")
    print("Valid periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца) или пробел для задания промежутка времени:»")

    csv_filename_choice = True  # True - filename генерируется автоматически; False - filename задается пользователем

    # Fetch stock data
    start = ''
    end = ''
    if period == ' ':
        start = input("Введите начало временного промежутка в формате гггг-мм-дд:»")
        end = input("Введите окончание временного промежутка в формате гггг-мм-дд:»")
    stock_data = dd.fetch_stock_data(ticker, period, start, end)

    # Сохраняет данные в CSV файл
    if csv_filename_choice:  # Выбор способа задания имени csv файла
        if period == ' ':
            csv_file = ticker + '_' + datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
        else:
            csv_file = ticker + '_' + period + '_' + datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
        # Пример: 'AAPL_1mo_20241206_1921.csv' или 'AAPL_20241206_1921.csv'
    else:
        csv_file = input('Введите имя файла без расширения: ') + '.csv'  # (требуется проверка ввода)
    dd.export_data_to_csv(stock_data, csv_file)

    # calculates average price
    data_avrg = dd.calculate_and_display_average_price(stock_data)
    if period == ' ':
        print(f'Среднее значение цены закрытия для {ticker} за промежуток времени с {start} по {end} составляет {data_avrg:.2f}')
    else:
        print(f'Среднее значение цены закрытия для {ticker} за {period} составляет {data_avrg:.2f}')

    # Оценка размаха колебаниий акций
    # Порог - 10%
    dd.notify_if_strong_fluctuations(stock_data, 10.0)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Расчет и создание индикатора RSI
    rsi_data = dd.calculate_rsi(stock_data)
    # Визуализация RSI
    dplt.plot_rsi(rsi_data, ticker)

    # Расчет и создание индикатора MACD
    macd_data = dd.calculate_macd(stock_data)
    # Визуализация MACD
    dplt.plot_macd(macd_data, ticker)


if __name__ == "__main__":
    main()
