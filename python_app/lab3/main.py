import csv
import sys
import statistics
from split_module import split_data

def read_data_from_file(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if rows and rows[0][0].lower() == 'time':
            rows = rows[1:]  # Пропускаем заголовок
        return rows

def calculate_statistics(chunk):
    values = [value for _, value in chunk]
    return {
        'count': len(values),
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'mode': statistics.mode(values)
    }

def main():
    if len(sys.argv) < 3:
        print("Использование: python main.py <файл.csv> <интервал_в_минутах>")
        return

    filename = sys.argv[1]
    interval = int(sys.argv[2])
    rows = read_data_from_file(filename)
    data_chunks = split_data(rows, interval)

    for chunk in data_chunks:
        if chunk:
            start = chunk[0][0].strftime('%H:%M')
            end = chunk[-1][0].strftime('%H:%M')
            stats = calculate_statistics(chunk)
            print(f"{start} - {end}: {stats}")

if __name__ == '__main__':
    main()

