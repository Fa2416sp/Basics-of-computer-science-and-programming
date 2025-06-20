import os
import pytest
import csv
from split_module import split_data
from main import read_data_from_file, calculate_statistics
from datetime import datetime, timedelta

# --- Вспомогательные фикстуры ---

@pytest.fixture
def sample_rows():
    return [
        ['1.0', '100'],
        ['1.1', '110'],
        ['1.2', '120'],
        ['1.4', '130'],
        ['2.0', '140']
    ]

@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.csv"
    with open(file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'value'])
        writer.writerows([
            ['1.0', '100'],
            ['1.2', '110'],
            ['1.4', '120'],
        ])
    return str(file)

# --- Тесты по заданию ---

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_data_from_file("nonexistent.csv")

def test_file_unreadable(tmp_path):
    file = tmp_path / "unreadable.csv"
    file.write_text("time,value\n1.0,100")
    file.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            read_data_from_file(str(file))
    finally:
        file.chmod(0o644)  # Восстановим права

def test_invalid_file_format(tmp_path):
    file = tmp_path / "binary_file.bin"
    file.write_bytes(b"\x00\xFF\x00\xFF")
    with pytest.raises(UnicodeDecodeError):
        read_data_from_file(str(file))

def test_one_column_row(tmp_path):
    file = tmp_path / "bad.csv"
    with open(file, "w") as f:
        f.write("time,value\n1.0\n")
    with pytest.raises(IndexError):
        split_data(read_data_from_file(str(file)), 5)

def test_non_numeric_data(tmp_path):
    file = tmp_path / "bad_data.csv"
    with open(file, "w") as f:
        f.write("time,value\nabc,xyz\n")
    with pytest.raises(ValueError):
        split_data(read_data_from_file(str(file)), 5)

def test_correct_split(sample_rows):
    result = split_data(sample_rows, 5)
    assert isinstance(result, list)
    assert all(isinstance(chunk, list) for chunk in result)

def test_correct_number_of_chunks(sample_rows):
    chunks = split_data(sample_rows, 10)
    assert len(chunks) == 4  # Ожидается 4 интервала с учётом разброса данных

def test_statistics_accuracy():
    chunk = [
        (datetime(2025, 1, 1, 0, 0), 10),
        (datetime(2025, 1, 1, 0, 5), 20),
        (datetime(2025, 1, 1, 0, 10), 30)
    ]
    stats = calculate_statistics(chunk)
    assert stats['count'] == 3
    assert stats['mean'] == 20
    assert stats['median'] == 20
    assert stats['mode'] == 10  # mode может быть неоднозначной — зависит от входа

# --- Дополнительные тесты ---

def test_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("time,value\n")
    rows = read_data_from_file(str(file))
    assert rows == []

def test_non_empty_chunks(sample_rows):
    chunks = split_data(sample_rows, 5)
    assert all(len(chunk) > 0 for chunk in chunks)

def test_split_boundary_alignment():
    rows = [
        ['0.0', '100'],
        ['0.083333', '110'],  # ровно 5 минут
        ['0.166667', '120']   # ровно 10 минут
    ]
    chunks = split_data(rows, 5)
    assert len(chunks) == 2  # значения на границе входят в следующий интервал

