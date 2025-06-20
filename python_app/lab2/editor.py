import sys
import os

class TextEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.clipboard = ""
        self.undo_stack = []
        self.modified = False

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.lines = f.read().splitlines()
        else:
            self.lines = []

    def save_state(self):
        self.undo_stack.append(self.lines.copy())
        self.modified = True

    def insert(self, text, row=None, col=None):
        self.save_state()
        if row is None:
            self.lines.append(text)
        else:
            row -= 1
            if row >= len(self.lines):
                self.lines.extend([''] * (row - len(self.lines) + 1))
            line = self.lines[row]
            if col is None:
                col = len(line)
            self.lines[row] = line[:col] + text + line[col:]

    def delete_all(self):
        self.save_state()
        self.lines = []

    def delete_row(self, row):
        if 0 < row <= len(self.lines):
            self.save_state()
            self.lines.pop(row - 1)
        else:
            print("Ошибка: номер строки не указан или неверен.")

    def delete_col(self, col):
        if col is None:
            print("Ошибка: номер столбца не указан.")
            return
        self.save_state()
        for i in range(len(self.lines)):
            if col <= len(self.lines[i]):
                self.lines[i] = self.lines[i][:col - 1] + self.lines[i][col:]

    def swap_rows(self, r1, r2):
        if 0 < r1 <= len(self.lines) and 0 < r2 <= len(self.lines):
            self.save_state()
            self.lines[r1 - 1], self.lines[r2 - 1] = self.lines[r2 - 1], self.lines[r1 - 1]
        else:
            print("Ошибка: неверные номера строк.")

    def undo(self, steps=1):
        for _ in range(steps):
            if self.undo_stack:
                self.lines = self.undo_stack.pop()
            else:
                print("Нечего отменять.")
                break

    def copy(self, row, start=None, end=None):
        if 0 < row <= len(self.lines):
            line = self.lines[row - 1]
            self.clipboard = line[start - 1:end] if start else line
        else:
            print("Ошибка: неправильный номер строки.")

    def paste(self, row):
        if 0 < row <= len(self.lines):
            self.save_state()
            self.lines[row - 1] += self.clipboard

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines))
        self.modified = False

    def show(self):
        for i, line in enumerate(self.lines, 1):
            print(f"{i}: {line}")

def main():
    if len(sys.argv) < 2:
        print("Укажите путь к файлу.")
        return

    editor = TextEditor(sys.argv[1])
    print("Командный редактор готов. Введите команду:")
    
    while True:
        command = input(">> ").strip()
        if command.startswith("insert"):
            parts = command.split('"')
            text = parts[1]
            args = parts[2].strip().split()
            row = int(args[0]) if len(args) > 0 else None
            col = int(args[1]) if len(args) > 1 else None
            editor.insert(text, row, col)
        elif command == "del":
            editor.delete_all()
        elif command.startswith("delrow"):
            try:
                _, row = command.split()
                editor.delete_row(int(row))
            except:
                print("Ошибка: укажите номер строки.")
        elif command.startswith("delcol"):
            try:
                _, col = command.split()
                editor.delete_col(int(col))
            except:
                print("Ошибка: укажите номер столбца.")
        elif command.startswith("swap"):
            try:
                _, r1, r2 = command.split()
                editor.swap_rows(int(r1), int(r2))
            except:
                print("Ошибка: укажите две строки.")
        elif command.startswith("undo"):
            parts = command.split()
            steps = int(parts[1]) if len(parts) > 1 else 1
            editor.undo(steps)
        elif command.startswith("copy"):
            parts = command.split()
            row = int(parts[1])
            start = int(parts[2]) if len(parts) > 2 else None
            end = int(parts[3]) if len(parts) > 3 else None
            editor.copy(row, start, end)
        elif command.startswith("paste"):
            try:
                _, row = command.split()
                editor.paste(int(row))
            except:
                print("Ошибка: укажите номер строки.")
        elif command == "save":
            editor.save()
        elif command == "show":
            editor.show()
        elif command == "exit":
            if editor.modified:
                confirm = input("Сохранить изменения перед выходом? (y/n): ")
                if confirm.lower() == 'y':
                    editor.save()
            print("Выход из редактора.")
            break
        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()

