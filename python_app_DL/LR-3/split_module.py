from datetime import datetime, timedelta   #тут мы группируем временные ряды данных по интервалам времени
                                            #с целью формирования временных окон фиксированной длительности
def split_data(rows, interval_minutes):
    grouped = []       #Список для накопления сгруппированных данных
    current_group = [] #Временный контейнер для накапливания элементов текущей группы
    start_time = None  #Начало временной группы

    for row in rows:   #проходим по временным рядам
        timestamp, value = float(row[0]), row[1] 

        if start_time is None:
            start_time = timestamp  #если группа ещё не создана (start_time is None), то стартовое время устанавливается на первую временную отметку
            current_group = [row]
        elif timestamp - start_time <= interval_minutes: #Если разница между текущей временной отметкой и началом последней группы меньше
            current_group.append(row) #или равна продолжительности интервала (interval_minutes), то строка добавляется в текущую группу
        else:
            grouped.append((start_time, timestamp, current_group)) #Если временное окно превышено, текущая группа фиксируется,
            start_time = timestamp                                 #а новое окно формируется заново
            current_group = [row]

    if current_group: #После прохода по всем данным, последняя сформированная группа добавляется в общий список
        grouped.append((start_time, timestamp, current_group))

    return grouped

