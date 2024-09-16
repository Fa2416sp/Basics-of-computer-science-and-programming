# Makefile для сборки программы dict1

# Компилятор
CC = gcc

# Флаги компилятора
CFLAGS = -Wall -Wextra -std=c99

# Имя исполняемого файла
TARGET = dict1

# Исходные файлы
SRCS = dict1.c

# Правило по умолчанию
all: $(TARGET)

# Правило сборки исполняемого файла
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

# Правило очистки
clean:
	rm -f $(TARGET)
