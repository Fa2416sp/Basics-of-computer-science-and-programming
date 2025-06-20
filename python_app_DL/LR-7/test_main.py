import pytest
import os #Взаимодействие с ОС, работа с путями
import csv #Библиотека для чтения и записи файлов формата CSV
from datetime import datetime
from main import read_data_from_file, calculate_statistics
from split_module import split_data #Внешний модуль, содержащий функцию split_data, которая разбивает данные на временные интервалы

# Тестовые данные
TEST_DATA = [
    ("1.04296875", "0"),
    ("1.75390625", "182"),
    ("2.46484375", "182"),
    ("3.1953125", "187"),
    ("3.92578125", "187"),
    ("4.69921875", "198"),
    ("5.48046875", "200"),
    ("6.27734375", "204"),
    ("7.07421875", "204"),
    ("7.85546875", "200"),
    ("8.6328125", "199"),
    ("9.359375", "186"),
    ("10.078125", "184"),
    ("10.75390625", "173"),
    ("11.42578125", "172"),
]

# Создание тестового CSV файла
def create_test_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "value"])
        for row in data:
            writer.writerow(row)

# Тесты для функции read_data_from_file
def test_read_data_from_file_valid(tmp_path):
    filename = tmp_path / "test.csv"
    create_test_csv(filename, TEST_DATA)
    data = read_data_from_file(filename)
    assert len(data) == len(TEST_DATA)
    assert data[0] == ("1.04296875", 0.0)
    assert data[-1] == ("11.42578125", 172.0)

#Тест отсутствия файла
def test_read_data_from_file_nonexistent():
    with pytest.raises(Exception):
        read_data_from_file("nonexistent.csv")

from unittest import mock

#Тест недостатка прав доступа
def test_read_data_from_file_no_permission(tmp_path):
    filename = tmp_path / "no_permission.csv"
    create_test_csv(filename, TEST_DATA)

    with mock.patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(PermissionError):
            read_data_from_file(filename)

#Тест неправильного формата файла
def test_read_data_from_file_invalid_format(tmp_path):
    filename = tmp_path / "invalid.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Это не CSV файл")
    with pytest.raises(Exception):
        read_data_from_file(filename)

#Тест пропущенной колонки
def test_read_data_from_file_missing_column(tmp_path):
    filename = tmp_path / "missing_column.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "value"])
        writer.writerow(["1.04296875"])  # Пропущено значение
    with pytest.raises(Exception):
        read_data_from_file(filename)

#Тест недопустимых данных
def test_read_data_from_file_invalid_type(tmp_path):
    filename = tmp_path / "invalid_type.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "value"])
        writer.writerow(["1.04296875", "abc"])  # Нечисловое значение
    with pytest.raises(Exception):
        read_data_from_file(filename)

# Тесты для функции split_data
def test_split_data_correct_intervals():
    data = [(str(float(i)), i) for i in range(10)]  # 0.0-9.0
    interval = 3
    result = split_data(data, interval)
    assert len(result) == 3
    assert result[0][0] == 0.0
    assert result[0][1] == 4.0
    assert result[-1][0] == 8.0

#Тест пустого ввода
def test_split_data_empty_input():
    assert split_data([], 5) == []

#Тест единственного интервала
def test_split_data_single_interval():
    data = [(str(float(i)), i) for i in range(5)]
    grouped_data = split_data(data, 10)
    assert len(grouped_data) == 1  # Все данные в одном интервале

# Тесты для функции calculate_statistics
def test_calculate_statistics(): #Тест базовой статистики
    chunk = [("1", 10), ("2", 20), ("3", 20), ("4", 40)]
    stats = calculate_statistics(chunk)
    assert stats['count'] == 4
    assert stats['mean'] == 22.5
    assert stats['median'] == 20.0
    assert stats['mode'] == 20

#Тест пустой группы
def test_calculate_statistics_empty_chunk():
    with pytest.raises(Exception):
        calculate_statistics([])

#Тест одиночной точки
def test_calculate_statistics_single_value():
    chunk = [("1", 10)]
    stats = calculate_statistics(chunk)
    assert stats['count'] == 1
    assert stats['mean'] == 10
    assert stats['median'] == 10
    assert stats['mode'] == 10

# Дополнительные тесты
def test_split_data_edge_intervals(): #Тест краевого случая интервалов
    data = [(str(float(i)), i) for i in range(5)]  # 0.0-4.0
    interval = 2
    result = split_data(data, interval)
    assert len(result) == 2
    assert result[0][0] == 0.0 and result[0][1] == 3.0
    assert result[-1][0] == 3.0 and result[-1][1] == 4.0

#Тест отрицательных значений
def test_calculate_statistics_negative_values():
    chunk = [("1", -10), ("2", -20), ("3", -20)]
    stats = calculate_statistics(chunk)
    assert stats['mean'] == -16.666666666666668
    assert stats['mode'] == -20

#Тест дробных значений
def test_calculate_statistics_floating_point():
    chunk = [("1", 1.5), ("2", 2.5), ("3", 2.5)]
    stats = calculate_statistics(chunk)
    assert stats['mean'] == 2.1666666666666665
    assert stats['mode'] == 2.5