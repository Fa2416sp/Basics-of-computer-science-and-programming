def split_data(rows, interval_minutes):
    grouped = []
    current_group = []
    start_time = None

    for row in rows:
        timestamp, value = float(row[0]), row[1]
                                                         # Логика группировки
        if start_time is None:                           # Во время прохода по ряду данных формируется следующая структура:
            start_time = timestamp     # Когда приходит новая запись, проверяется, входит ли она в диапазон текущего временного окна (timestamp - start_time <= interval_minutes)
            current_group = [row]                        # Если запись укладывается в интервал, она добавляется в текущую группу
        elif timestamp - start_time <= interval_minutes: # Если запись выпадает за рамки интервала, текущая группа фиксируется,
            current_group.append(row)                    # и начинается новая группа с новым временным окном
        else:                #В результате получается список, каждый элемент которого представляет собой кортеж: начало,конец,список строк
            grouped.append((start_time, timestamp, current_group))
            start_time = timestamp
            current_group = [row]

    if current_group:
        grouped.append((start_time, timestamp, current_group))

    return grouped

