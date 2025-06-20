import sys #Стандартная библиотека Python, используемая для доступа к аргументам командной строки
import csv #Библиотека для чтения и записи файлов формата CSV
from statistics import mean, median, mode #Модуль для расчета базовых статистик, таких как среднее, медиана и мода
from split_module import split_data #Внешний модуль, содержащий функцию split_data, которая разбивает данные на временные интервалы

def read_data_from_file(filename): #читаем данные из CSV-файла и формируем список кортежей, где каждое значение представляет собой пару (timestamp, value)
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) #пропускаем заголовочную строку
        return [(row[0], float(row[1])) for row in reader if row] #преобразуем значения второго столбца в вещественное число

def calculate_statistics(chunk): #вычисление статистики для одного блока данных
    values = [value for _, value in chunk]
    return {
        'count': len(values),
        'mean': mean(values),
        'median': median(values),
        'mode': mode(values),
    }

def main():
    if len(sys.argv) < 3:
        print("Использование: python main.py <имя_файла.csv> <интервал_в_минутах>")
        return

    filename = sys.argv[1]
    interval_minutes = int(sys.argv[2])

    try:
        data = read_data_from_file(filename) #чтение данных из файла
        grouped_data = split_data(data, interval_minutes) #данные делятся на блоки

        for start, end, group in grouped_data: #вычисляются статистические характеристики
            stats = calculate_statistics(group) 
            print(f"\nИнтервал {start} — {end}")
            print(f"Количество: {stats['count']}")
            print(f"Среднее: {stats['mean']}")
            print(f"Медиана: {stats['median']}")
            print(f"Мода: {stats['mode']}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
