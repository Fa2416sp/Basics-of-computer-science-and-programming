from flask import Flask, render_template, request

app = Flask(__name__)

WIDTH, HEIGHT = 100, 100

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    error = ""
    if request.method == 'POST':
        commands_text = request.form['commands']
        commands = [line.strip().upper() for line in commands_text.splitlines()]
        x, y = 1, 1
        path = []
        history = []
        valid = True

        try:
            for command in commands:
                if command == "E":
                    break
                parts = command.split()
                if parts[0] == "B":
                    steps = int(parts[1]) if len(parts) > 1 else 1
                    real_history = [h for h in history if h[0] != "B"]
                    if len(real_history) < steps:
                        error = "Недостаточно истории для возврата"
                        valid = False
                        break
                    for i in range(steps):
                        dir_, cnt = real_history.pop()
                        dx, dy = get_back_step(dir_)
                        for _ in range(cnt):
                            x += dx
                            y += dy
                            if not is_in_bounds(x, y):
                                valid = False
                                error = "Робот вышел за границы поля"
                                break
                            path.append(f"{x},{y}")
                    history.append(("B", steps))
                else:
                    dir_, count = parts[0], int(parts[1])
                    dx, dy = get_delta(dir_)
                    for _ in range(count):
                        x += dx
                        y += dy
                        if not is_in_bounds(x, y):
                            valid = False
                            error = "Робот вышел за границы поля"
                            break
                        path.append(f"{x},{y}")
                    history.append((dir_, count))
                if not valid:
                    break
        except:
            valid = False
            error = "Ошибка обработки команд"

        result = path if valid else []
    return render_template('index.html', result=result, error=error)


def get_delta(direction):
    return {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1)
    }.get(direction, (0, 0))

def get_back_step(direction):
    dx, dy = get_delta(direction)
    return -dx, -dy

def is_in_bounds(x, y):
    return 1 <= x <= WIDTH and 1 <= y <= HEIGHT

if __name__ == '__main__':
    app.run(debug=True)

