import os #Взаимодействие с ОС, работа с путями
import random #генерация случайных чисел
import string #работа со строками
import shutil #упрощает работу с файлами и каталогами на уровне ОС
from pathlib import Path #объектно-ориентированный API для работы с путями к файлам и каталогам.

def generate_random_content(min_size=10, max_size=1000): #генерирует произвольную строку из случайных букв и цифр
    """Генерирует случайное содержимое для файла"""
    size = random.randint(min_size, max_size)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def create_test_structure(root_dir):
    """Создает тестовую файловую структуру с дубликатами"""
    root = Path(root_dir)
    
    # Очищаем и создаем корневую директорию
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    
    # Создаем несколько уникальных файлов
    for i in range(3):
        with open(root / f"unique_file_{i}.txt", 'w') as f:
            f.write(generate_random_content())
    
    # Создаем группу дубликатов с одинаковыми именами
    content = generate_random_content()
    for i in range(3):
        with open(root / f"duplicate_same_name_{i}.txt", 'w') as f:
            f.write(content)
    
    # Создаем группу дубликатов с разными именами
    content = generate_random_content()
    names = ["copy1.dat", "data.bin", "backup.txt", "file_123.tmp"]
    for name in names[:3]:  # создаем 3 дубликата
        with open(root / name, 'w') as f:
            f.write(content)
    
    # Создаем подкаталоги с дубликатами
    subdirs = ["docs", "backup", "temp"]
    for i, dirname in enumerate(subdirs):
        dirpath = root / dirname
        dirpath.mkdir()
        
        # Уникальные файлы в подкаталогах
        with open(dirpath / f"sub_unique_{i}.txt", 'w') as f:
            f.write(generate_random_content())
        
        # Дубликаты внутри подкаталогов
        if i < 2:  # создаем в первых двух подкаталогах
            with open(dirpath / "duplicate_in_subdir.txt", 'w') as f:
                f.write(content)
        
        # Дубликаты между подкаталогами и корнем
        if i == 0:  # только для первого подкаталога
            with open(dirpath / "duplicate_with_root.txt", 'w') as f:
                f.write(content)
    
    # Создаем дубликат файла из корня в подкаталоге
    with open(root / "duplicate_with_root.txt", 'w') as f:
        f.write(content)
    
    # Создаем большой дубликат (для теста производительности)
    big_content = generate_random_content(5000, 10000)
    with open(root / "big_file.bin", 'w') as f:
        f.write(big_content)
    with open(root / "backup" / "big_file_copy.bin", 'w') as f:
        f.write(big_content)
    
    # Создаем пустые файлы-дубликаты
    for i in range(2):
        with open(root / f"empty_file_{i}.tmp", 'w') as f:
            pass
    
    print(f"Тестовая структура создана в {root.absolute()}")

if __name__ == "__main__":
    test_dir = "test_fdupes"
    create_test_structure(test_dir)