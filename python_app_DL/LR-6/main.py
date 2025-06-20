import os #Взаимодействие с ОС, работа с путями
import hashlib #интерфейс для различных хеш-функций
import sys #Стандартная библиотека Python, используемая для доступа к аргументам командной строки
from collections import defaultdict #Упрощает работу со словарями, автоматически назначая значение по умолчанию для несуществующих ключей

def get_file_hash(filepath, block_size=65536):
    """Вычисляет хеш SHA-256 содержимого файла"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicates(root_dir):
    """Находит все дубликаты файлов в указанном каталоге и его подкаталогах"""
    files_by_size = defaultdict(list)
    files_by_hash = defaultdict(list)
    
    # Сначала группируем файлы по размеру (быстрая проверка)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(full_path)
                files_by_size[file_size].append(full_path)
            except OSError:
                continue
    
    # Затем проверяем хеш файлов с одинаковым размером
    for file_size, files in files_by_size.items():  #Сначала файлы сортируются по размерам, так как сравнивать хеши файлов разного размера бессмысленно.
        if len(files) > 1:    #Потом вычисляются хеши для файлов с одинаковым размером.
            for filepath in files: #Те файлы, у которых совпадают и размер, и хеш, определяются как дубликаты.
                try:
                    file_hash = get_file_hash(filepath)
                    files_by_hash[(file_size, file_hash)].append(filepath)
                except OSError:
                    continue
    
    # Возвращаем только группы с дубликатами
    return [files for files in files_by_hash.values() if len(files) > 1]

def handle_duplicates(duplicates):
    """Обрабатывает найденные дубликаты, предлагая пользователю выбор"""
    for group in duplicates:
        print(f"\nНайдены дубликаты ({len(group)} файлов):")
        for i, filepath in enumerate(group, 1):
            print(f"{i}: {filepath}")
        
        while True:
            choice = input("\nВыберите файл для сохранения (1-{0}), "
                          "'all' чтобы оставить все, 'skip' чтобы пропустить: "
                          .format(len(group))).strip().lower()
            
            if choice == 'skip':
                print("Пропускаем эту группу...")
                break
            elif choice == 'all':
                print("Оставляем все файлы в этой группе...")
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(group):
                file_to_keep = group[int(choice)-1]
                for filepath in group:
                    if filepath != file_to_keep:
                        try:
                            os.remove(filepath)
                            print(f"Удалён: {filepath}")
                        except OSError as e:
                            print(f"Ошибка при удалении {filepath}: {e}")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

def main():
    if len(sys.argv) != 2:
        print("Использование: python fdupes.py <каталог>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"Ошибка: {root_dir} не является каталогом или не существует")
        sys.exit(1)
    
    print(f"Поиск дубликатов в каталоге: {root_dir}...")
    duplicates = find_duplicates(root_dir)
    
    if not duplicates:
        print("Дубликаты не найдены.")
        return
    
    print(f"\nНайдено {len(duplicates)} групп дубликатов.")
    handle_duplicates(duplicates)

if __name__ == "__main__":
    main()