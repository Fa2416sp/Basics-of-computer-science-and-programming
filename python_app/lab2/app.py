from flask import Flask, render_template, request, redirect
from editor import TextEditor

app = Flask(__name__)
editor = TextEditor("web_text.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        command = request.form["command"]
        output = handle_command(command)
    return render_template("index.html", lines=editor.lines, output=output)

def handle_command(command):
    try:
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
            editor.delete_row(int(command.split()[1]))
        elif command.startswith("delcol"):
            editor.delete_col(int(command.split()[1]))
        elif command.startswith("swap"):
            _, r1, r2 = command.split()
            editor.swap_rows(int(r1), int(r2))
        elif command.startswith("undo"):
            steps = int(command.split()[1]) if len(command.split()) > 1 else 1
            editor.undo(steps)
        elif command.startswith("copy"):
            parts = command.split()
            row = int(parts[1])
            start = int(parts[2]) if len(parts) > 2 else None
            end = int(parts[3]) if len(parts) > 3 else None
            editor.copy(row, start, end)
        elif command.startswith("paste"):
            editor.paste(int(command.split()[1]))
        elif command == "save":
            editor.save()
        elif command == "show":
            return "Файл:\n" + "\n".join(f"{i+1}: {l}" for i, l in enumerate(editor.lines))
        elif command == "exit":
            return "Выйти невозможно через веб-интерфейс :)"
        else:
            return "Неизвестная команда."
        return "Команда выполнена."
    except Exception as e:
        return f"Ошибка: {e}"

if __name__ == "__main__":
    app.run(debug=True)

