def parse_high_level_program(program_lines): #Принимаем список строк
    commands = [] #Создаем пустой список для хранения разобранных команд
    for line in program_lines:
        line = line.strip()  #Обрабатываем, очищаем от пробелов и запятых
        if not line:
            continue
        if line.startswith("B"):
            parts = line.split(',')
            count = int(parts[1]) if len(parts) == 2 else 1
            commands.append(('B', count)) #Добавляем специальную команду в виде кортежа ('B', count)
        else:
            direction, steps = line.split(',')
            commands.append((direction.strip(), int(steps.strip())))
    return commands #Возвращаем итоговый список команд


def move_robot(commands):
    x, y = 1, 1 #Стартовая позиция
    path = [] #Финальный путь перемещений
    history = [(x, y)] #История посещенных координат 

    for command in commands:
        direction, value = command        #Перебираем каждую команду из списка commands циклом

        if direction in ('R', 'L', 'U', 'D'):
            dx, dy = 0, 0
            if direction == 'R':
                dx = 1
            elif direction == 'L':
                dx = -1
            elif direction == 'U':
                dy = -1
            elif direction == 'D':
                dy = 1

            for _ in range(value):
                x += dx
                y += dy
                if not (1 <= x <= 100 and 1 <= y <= 100):
                    return None, f"Ошибка: выход за границы поля в точке ({x},{y})"
                history.append((x, y))
                path.append((x, y))

        elif direction == 'B':
            if value >= len(history):
                return None, f"Ошибка: нельзя вернуться на {value} шагов, в истории только {len(history) - 1}"

            steps_back = history[-(value + 1):-1][::-1]
            for step in steps_back:
                x, y = step
                history.append((x, y))
                path.append((x, y))

    return path, None


def main():
    print("Введите высокоуровневую программу. Пустая строка — завершение.") #Вводим
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)

    try:
        commands = parse_high_level_program(lines)             #Парсим
    except Exception as e:
        print(f"Ошибка разбора: {e}")
        return

    path, error = move_robot(commands) #Идём
    if error:
        print(error)
    else:
        for x, y in path:
            print(f"{x},{y}")


if __name__ == "__main__":
    main()
