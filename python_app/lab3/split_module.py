from datetime import datetime, timedelta

def split_data(rows, interval_minutes):
    chunks = []
    current_chunk = []

    if not rows:
        return chunks

    base_time = datetime(2025, 1, 1, 0, 0)  # Базовая точка отсчёта
    start_time = base_time + timedelta(hours=float(rows[0][0]))
    end_time = start_time + timedelta(minutes=interval_minutes)

    for row in rows:
        timestamp = base_time + timedelta(hours=float(row[0]))
        value = float(row[1])

        if timestamp < end_time:
            current_chunk.append((timestamp, value))
        else:
            chunks.append(current_chunk)
            current_chunk = [(timestamp, value)]
            start_time = timestamp
            end_time = start_time + timedelta(minutes=interval_minutes)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

