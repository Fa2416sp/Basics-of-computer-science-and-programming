# -*- coding: utf-8 -*-
import os
import hashlib

def get_file_hash(file_path):
    """Возвращает SHA-256 хеш файла"""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return None

def find_duplicates(directory):
    """Находит дубликаты в указанной директории"""
    hashes = {}
    duplicates = {}

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash:
                if file_hash in hashes:
                    duplicates.setdefault(file_hash, []).append(file_path)
                else:
                    hashes[file_hash] = file_path

    return duplicates

def main():
    directory = input("Введите путь к каталогу: ").strip()
    if not os.path.exists(directory):
        print("Каталог не найден.")
        return

    duplicates = find_duplicates(directory)

    if not duplicates:
        print("Дубликаты не найдены.")
        return

    print("\nНайденные дубликаты:")
    for file_hash, paths in duplicates.items():
        print(f"\nХеш: {file_hash}")
        for i, path in enumerate(paths):
            print(f"{i+1}: {path}")
        
        choice = input("Введите номера файлов для удаления (через запятую), либо Enter для пропуска: ").strip()
        if choice:
            for index in choice.split(","):
                try:
                    index = int(index) - 1
                    os.remove(paths[index])
                    print(f"Удалён: {paths[index]}")
                except (ValueError, IndexError):
                    print(f"Некорректный ввод: {index}")

if __name__ == "__main__":
    main()

