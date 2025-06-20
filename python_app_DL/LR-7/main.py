import sys #Стандартная библиотека Python, используемая для доступа к аргументам командной строки
import csv #Библиотека для чтения и записи файлов формата CSV
from statistics import mean, median, mode #Модуль для расчета базовых статистик, таких как среднее, медиана и мода
from split_module import split_data #Внешний модуль, содержащий функцию split_data, которая разбивает данные на временные интервалы

def read_data_from_file(filename): #Функция читает CSV-файл и проверяет его формат
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header != ["time", "value"]:
            raise ValueError("Файл не соответствует формату CSV: ожидались колонки 'time,value'")
        data = []
        for row in reader:
            if len(row) != 2:
                raise ValueError(f"Некорректная строка: {row}. Ожидалось 2 колонки.")
            try:
                data.append((row[0], float(row[1])))
            except ValueError:
                raise ValueError(f"Некорректное значение: {row[1]}. Ожидалось число.")
        return data

def calculate_statistics(chunk): #вычисляет базовые статистические показатели для каждого временного интервала
    values = [value for _, value in chunk]
    return {
        'count': len(values),
        'mean': mean(values),
        'median': median(values),
        'mode': mode(values),
    }

def main(): #главная функция программы, обрабатывающая командную строку и производящая расчеты
    if len(sys.argv) < 3:
        print("Использование: python main.py <имя_файла.csv> <интервал_в_минутах>")
        return

    filename = sys.argv[1]
    interval_minutes = int(sys.argv[2])

    try:
        data = read_data_from_file(filename)  #Данные читаются из файла, потом разбиваются на временные интервалы с помощью функции split_data
        grouped_data = split_data(data, interval_minutes)

        for start, end, group in grouped_data:
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
