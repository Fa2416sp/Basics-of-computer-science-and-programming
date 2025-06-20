import pygame
import random
import time
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Настройки по умолчанию
DEFAULT_BOARD_SIZE = 10
CELL_SIZE = 40
MARGIN = 50
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 150

class Block:
    def __init__(self, block_type, rotation=0):
        self.block_type = block_type  # 'vertical', 'horizontal', 'corner'
        self.rotation = rotation  # 0, 1, 2, 3 (0, 90, 180, 270 degrees)
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        
    def get_connections(self):
        """Возвращает направления, в которые ведут соединения блока"""
        if self.block_type == 'vertical':
            if self.rotation in (0, 2):
                return ['top', 'bottom']
            else:
                return ['left', 'right']
        elif self.block_type == 'horizontal':
            if self.rotation in (0, 2):
                return ['left', 'right']
            else:
                return ['top', 'bottom']
        elif self.block_type == 'corner':
            if self.rotation == 0:
                return ['right', 'bottom']
            elif self.rotation == 1:
                return ['top', 'right']
            elif self.rotation == 2:
                return ['top', 'left']
            else:  # rotation == 3
                return ['left', 'bottom']
    
    def draw(self, surface, x, y, size, lit=False):
        """Отрисовка блока"""
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(surface, YELLOW if lit else WHITE, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        center_x, center_y = x + size // 2, y + size // 2
        connections = self.get_connections()
        
        if 'top' in connections:
            pygame.draw.line(surface, BLUE, (center_x, center_y), (center_x, y), 3)
        if 'bottom' in connections:
            pygame.draw.line(surface, BLUE, (center_x, center_y), (center_x, y + size), 3)
        if 'left' in connections:
            pygame.draw.line(surface, BLUE, (center_x, center_y), (x, center_y), 3)
        if 'right' in connections:
            pygame.draw.line(surface, BLUE, (center_x, center_y), (x + size, center_y), 3)

class Game:
    def __init__(self, board_size=DEFAULT_BOARD_SIZE):
        self.board_size = board_size
        self.reset_game()
        
    def reset_game(self):
        """Сброс игры с текущим размером поля"""
        self.board = []
        self.generate_board()
        self.lit_cells = set()
        self.game_over = False
        self.win = False
        self.start_time = time.time()
        self.time_limit = 120  # 2 минуты в секундах
        self.update_lit_cells()
        
    def generate_board(self):
        """Генерация случайного игрового поля"""
        self.board = []
        for row in range(self.board_size):
            board_row = []
            for col in range(self.board_size):
                # Первый и последний столбцы - угловые блоки
                if col == 0 or col == self.board_size - 1:
                    block_type = 'corner'
                else:
                    block_type = random.choice(['vertical', 'horizontal'])
                
                # Случайный поворот
                rotation = random.randint(0, 3)
                board_row.append(Block(block_type, rotation))
            self.board.append(board_row)
    
    def update_lit_cells(self):
        """Обновление подсвеченных клеток"""
        new_lit = set()
        queue = [(0, 0)]  # Начинаем с левой верхней клетки
        visited = set()
        
        while queue:
            row, col = queue.pop(0)
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            new_lit.add((row, col))
            
            # Получаем соединения текущего блока
            block = self.board[row][col]
            connections = block.get_connections()
            
            # Проверяем соседние клетки
            if 'top' in connections and row > 0:
                neighbor_block = self.board[row-1][col]
                if 'bottom' in neighbor_block.get_connections():
                    queue.append((row-1, col))
                    
            if 'bottom' in connections and row < self.board_size - 1:
                neighbor_block = self.board[row+1][col]
                if 'top' in neighbor_block.get_connections():
                    queue.append((row+1, col))
                    
            if 'left' in connections and col > 0:
                neighbor_block = self.board[row][col-1]
                if 'right' in neighbor_block.get_connections():
                    queue.append((row, col-1))
                    
            if 'right' in connections and col < self.board_size - 1:
                neighbor_block = self.board[row][col+1]
                if 'left' in neighbor_block.get_connections():
                    queue.append((row, col+1))
        
        self.lit_cells = new_lit
        
        # Проверка победы
        if len(self.lit_cells) == self.board_size * self.board_size:
            self.game_over = True
            self.win = True
    
    def rotate_block(self, row, col):
        """Поворот блока по указанным координатам"""
        if not self.game_over:
            self.board[row][col].rotate()
            self.update_lit_cells()
    
    def check_time(self):
        """Проверка оставшегося времени"""
        if not self.game_over:
            elapsed = time.time() - self.start_time
            if elapsed >= self.time_limit:
                self.game_over = True
                self.win = False
            return max(0, self.time_limit - elapsed)
        return 0
    
    def solve_board(self):
        """Решение головоломки (для показа после проигрыша)"""
        # Простая стратегия: поворачиваем все блоки, чтобы они соединялись
        for row in range(self.board_size):
            for col in range(self.board_size):
                block = self.board[row][col]
                
                # Для угловых блоков в первом и последнем столбце
                if col == 0 or col == self.board_size - 1:
                    if col == 0:
                        # Левый столбец - соединение направо
                        while 'right' not in block.get_connections():
                            block.rotate()
                    else:
                        # Правый столбец - соединение налево
                        while 'left' not in block.get_connections():
                            block.rotate()
                else:
                    # Остальные блоки - вертикальные или горизонтальные
                    if block.block_type == 'vertical':
                        while 'top' not in block.get_connections() or 'bottom' not in block.get_connections():
                            block.rotate()
                    else:  # horizontal
                        while 'left' not in block.get_connections() or 'right' not in block.get_connections():
                            block.rotate()
        
        self.update_lit_cells()

class GameUI: #Устанавливает размеры окна и создает поверхность для рисования
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Light'em up!")
        
        #таймер и шрифты
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Клетки
        self.game = Game()
        self.cell_size = CELL_SIZE
        self.board_offset_x = (self.screen_width - self.game.board_size * self.cell_size) // 2
        self.board_offset_y = (self.screen_height - self.game.board_size * self.cell_size) // 2
        
        # Кнопки
        self.reset_button = pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.settings_button = pygame.Rect(20, 70, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Настройки
        self.settings_active = False
        self.size_input = str(DEFAULT_BOARD_SIZE)
        self.size_input_active = False
        self.size_input_rect = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2, 100, 30)
        self.apply_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 50, 100, 30)
    
    def handle_events(self): # обработка события закрытия окна, кликов мыши и нажатий клавиш
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.handle_click(event.pos)
                    
            if event.type == KEYDOWN and self.settings_active and self.size_input_active:
                if event.key == K_RETURN:
                    self.apply_settings()
                elif event.key == K_BACKSPACE:
                    self.size_input = self.size_input[:-1]
                elif event.unicode.isdigit() and len(self.size_input) < 3:
                    self.size_input += event.unicode
    
    def handle_click(self, pos): #Определяет, какая часть экрана была нажата (игровое поле, кнопки "Новую игру" или "Настройки")
        if self.settings_active:
            if self.size_input_rect.collidepoint(pos):
                self.size_input_active = True
            else:
                self.size_input_active = False
                
            if self.apply_button.collidepoint(pos):
                self.apply_settings()
        else:
            # Проверка клика по игровому полю
            if (self.board_offset_x <= pos[0] <= self.board_offset_x + self.game.board_size * self.cell_size and
                self.board_offset_y <= pos[1] <= self.board_offset_y + self.game.board_size * self.cell_size):
                
                if not self.game.game_over:
                    col = (pos[0] - self.board_offset_x) // self.cell_size
                    row = (pos[1] - self.board_offset_y) // self.cell_size
                    self.game.rotate_block(row, col)
            
            # Проверка клика по кнопкам
            if self.reset_button.collidepoint(pos):
                self.game.reset_game()
            elif self.settings_button.collidepoint(pos):
                self.settings_active = True
                self.size_input = str(self.game.board_size)
    
    def apply_settings(self): #Применяет изменения в размере игрового поля и сбрасывает игру
        try:
            new_size = int(self.size_input)
            if 10 <= new_size <= 100:
                self.game.board_size = new_size
                self.game.reset_game()
                # Обновляет размеры отображения
                max_cell_size = min(
                    (self.screen_width - 100) // new_size,
                    (self.screen_height - 100) // new_size
                )
                self.cell_size = max(10, max_cell_size)
                self.board_offset_x = (self.screen_width - self.game.board_size * self.cell_size) // 2
                self.board_offset_y = (self.screen_height - self.game.board_size * self.cell_size) // 2
        except ValueError:
            pass
        
        self.settings_active = False
    
    def draw(self): #Основной метод рисования. Переключает между режимами: игровая сцена или окно настроек
        self.screen.fill(LIGHT_GRAY)
        
        if self.settings_active:
            self.draw_settings()
        else:
            self.draw_game()
        
        pygame.display.flip()
    
    def draw_settings(self): 
        # Затемнение фона
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))
        
        # Окно настроек
        settings_rect = pygame.Rect(
            self.screen_width // 4,
            self.screen_height // 4,
            self.screen_width // 2,
            self.screen_height // 2
        )
        pygame.draw.rect(self.screen, WHITE, settings_rect)
        pygame.draw.rect(self.screen, BLACK, settings_rect, 2)
        
        # Заголовок
        title = self.font.render("Настройки", True, BLACK)
        self.screen.blit(title, (settings_rect.centerx - title.get_width() // 2, settings_rect.y + 20))
        
        # Поле ввода размера
        label = self.small_font.render("Размер поля (10-100):", True, BLACK)
        self.screen.blit(label, (settings_rect.centerx - label.get_width() // 2, settings_rect.y + 70))
        
        pygame.draw.rect(self.screen, WHITE, self.size_input_rect)
        pygame.draw.rect(self.screen, BLUE if self.size_input_active else BLACK, self.size_input_rect, 2)
        input_text = self.font.render(self.size_input, True, BLACK)
        self.screen.blit(input_text, (self.size_input_rect.x + 5, self.size_input_rect.y + 5))
        
        # Кнопка применения
        pygame.draw.rect(self.screen, GRAY, self.apply_button)
        pygame.draw.rect(self.screen, BLACK, self.apply_button, 2)
        apply_text = self.font.render("Применить", True, BLACK)
        self.screen.blit(apply_text, (self.apply_button.centerx - apply_text.get_width() // 2, 
                                     self.apply_button.centery - apply_text.get_height() // 2))
    
    def draw_game(self):
        # Отрисовка игрового поля
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                x = self.board_offset_x + col * self.cell_size
                y = self.board_offset_y + row * self.cell_size
                is_lit = (row, col) in self.game.lit_cells
                self.game.board[row][col].draw(self.screen, x, y, self.cell_size, is_lit)
        
        # Отрисовка кнопок
        pygame.draw.rect(self.screen, GRAY, self.reset_button)
        pygame.draw.rect(self.screen, BLACK, self.reset_button, 2)
        reset_text = self.font.render("Новая игра", True, BLACK)
        self.screen.blit(reset_text, (self.reset_button.centerx - reset_text.get_width() // 2, 
                                      self.reset_button.centery - reset_text.get_height() // 2))
        
        pygame.draw.rect(self.screen, GRAY, self.settings_button)
        pygame.draw.rect(self.screen, BLACK, self.settings_button, 2)
        settings_text = self.font.render("Настройки", True, BLACK)
        self.screen.blit(settings_text, (self.settings_button.centerx - settings_text.get_width() // 2, 
                                        self.settings_button.centery - settings_text.get_height() // 2))
        
        # Отрисовка таймера
        time_left = self.game.check_time()
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        timer_text = self.font.render(f"Время: {minutes:02d}:{seconds:02d}", True, BLACK)
        self.screen.blit(timer_text, (self.screen_width - timer_text.get_width() - 20, 20))
        
        # Отрисовка сообщений о победе/проигрыше
        if self.game.game_over:
            if self.game.win:
                self.show_message("Победа!", "Вы успешно подсветили все клетки!")
            else:
                self.show_message("Время вышло!", "Вы не успели подсветить все клетки.")
                # Показываем решение
                self.game.solve_board()
    
    def show_message(self, title, message):
        # Затемнение фона
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))
        
        # Окно сообщения
        message_rect = pygame.Rect(
            self.screen_width // 4,
            self.screen_height // 3,
            self.screen_width // 2,
            self.screen_height // 3
        )
        pygame.draw.rect(self.screen, WHITE, message_rect)
        pygame.draw.rect(self.screen, BLACK, message_rect, 2)
        
        # Заголовок
        title_text = self.font.render(title, True, BLACK)
        self.screen.blit(title_text, (message_rect.centerx - title_text.get_width() // 2, message_rect.y + 20))
        
        # Сообщение
        msg_text = self.small_font.render(message, True, BLACK)
        self.screen.blit(msg_text, (message_rect.centerx - msg_text.get_width() // 2, message_rect.centery - 10))
        
        # Кнопка OK
        ok_button = pygame.Rect(
            message_rect.centerx - 50,
            message_rect.y + message_rect.height - 50,
            100, 30
        )
        pygame.draw.rect(self.screen, GRAY, ok_button)
        pygame.draw.rect(self.screen, BLACK, ok_button, 2)
        ok_text = self.small_font.render("OK", True, BLACK)
        self.screen.blit(ok_text, (ok_button.centerx - ok_text.get_width() // 2, 
                                  ok_button.centery - ok_text.get_height() // 2))
        
        pygame.display.flip()
        
        # Ждем нажатия кнопки OK
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if ok_button.collidepoint(event.pos):
                        waiting = False
            self.clock.tick(30)
    
    def run(self):
        while True:
            self.handle_events() # События
            self.draw() # Графика
            self.clock.tick(30) # FPS

if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.run()