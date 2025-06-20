import sys  #для доступа к параметрам командной строки
import copy #для безопасного сохранения копий изменяемых объектов

def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: #загружаем файл 
            return f.read().splitlines() #Читаем содержимое и разделяем его на отдельные строки
    except FileNotFoundError:
        return []

def save_file(path, lines):                       #сохраняем список строк в файл,
    with open(path, 'w', encoding='utf-8') as f:  #объединяя элементы списка
        f.write('\n'.join(lines))

def print_lines(lines):
    for i, line in enumerate(lines, 1):  #Нумеруем строки 
        print(f"{i}: {line}")

def main():
    if len(sys.argv) < 2:
        print("Укажите путь к файлу при запуске.")
        return

    file_path = sys.argv[1] #Получаем путь к файлу из первого аргумента
    lines = load_file(file_path) #Загружаем исходный файл в список строк
    history = [] #Создаем пустой список для сохранения изменений

    while True:
        command = input(">> ").strip()

        if not command:
            continue

        parts = command.split() #Входная команда разделяется на составляющие
        cmd = parts[0]

        # Сохраняем состояние перед изменением
        if cmd in {"insert", "del", "delrow", "delcol", "swap"}: #Перед исполнением любой команды, меняющей содержимое файла,
            history.append(copy.deepcopy(lines))                 #делается глубокая копия текущих строк и сохраняется в список history
                                                                 #это обеспечит возможность последующего отката изменений.
        if cmd == "insert":
            if len(parts) < 2 or not parts[1].startswith('"') or not parts[1].endswith('"'):
                print("Ошибка: текст для вставки должен быть в двойных кавычках.")
                continue
            text = parts[1][1:-1]
            row = int(parts[2]) - 1 if len(parts) >= 3 else len(lines)
            col = int(parts[3]) - 1 if len(parts) == 4 else None

            while len(lines) <= row: #Если номер строки больше длины списка строк
                lines.append("")     #добавляем пустые строки

            if col is None:
                lines[row] += text   #по умолчанию вставляем текст в конец строки 
            else:
                lines[row] = lines[row][:col] + text + lines[row][col:]  #или вставляем текст в указанную позицию

        elif cmd == "del":
            lines = []

        elif cmd == "delrow":
            if len(parts) < 2:
                print("Ошибка: укажите номер строки.")
                continue
            row = int(parts[1]) - 1
            if 0 <= row < len(lines):
                lines.pop(row) #удаляем указанную строку
            else:
                print("Ошибка: неверный номер строки.")

        elif cmd == "delcol":
            if len(parts) < 2:
                print("Ошибка: укажите номер столбца.")
                continue
            col = int(parts[1]) - 1
            for i in range(len(lines)):  #пробегаемся по всем строкам
                if col < len(lines[i]):
                    lines[i] = lines[i][:col] + lines[i][col+1:] #удаляем указанный символ

        elif cmd == "swap":
            if len(parts) < 3:
                print("Ошибка: укажите два номера строк.")
                continue
            r1, r2 = int(parts[1]) - 1, int(parts[2]) - 1
            if 0 <= r1 < len(lines) and 0 <= r2 < len(lines):
                lines[r1], lines[r2] = lines[r2], lines[r1] #обмен строк местами
            else:
                print("Ошибка: один из номеров строк вне диапазона.")

        elif cmd == "undo":
            count = int(parts[1]) if len(parts) > 1 else 1
            for _ in range(min(count, len(history))):
                lines = history.pop()  #восстанавливаем предыдущую версию файла

        elif cmd == "save":
            save_file(file_path, lines)
            print("Файл сохранён.")

        elif cmd == "show":
            print_lines(lines)

        elif cmd == "exit":
            break

        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()
