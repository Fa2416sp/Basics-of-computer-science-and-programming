import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import random
from PIL import Image

class Cell:
    def __init__(self, cell_type, angle, highlighted=False):
        self.cell_type = cell_type
        self.angle = angle
        self.highlighted = highlighted

    def is_connected(self, other_cell, x1, y1, x2, y2):
        if self.cell_type == "угловая" and other_cell.cell_type == "угловая":
            if x1 > x2 and (self.angle == 90 or self.angle == 180):
                if other_cell.angle == 270 or other_cell.angle == 0:
                    return True
            if x1 < x2 and (self.angle == 270 or self.angle == 0):
                if other_cell.angle == 90 or other_cell.angle == 180:
                    return True
            return False
        if self.cell_type == "угловая" and other_cell.cell_type == "прямая" or self.cell_type == "прямая" and other_cell.cell_type == "угловая":
            if self.cell_type == "прямая" and (self.angle == 270 or self.angle == 90):
                if y1 < y2:
                    if other_cell.angle == 180 or other_cell.angle == 270:
                        return True
                if y1 > y2:
                    if other_cell.angle == 0 or other_cell.angle == 90:
                        return True
            if self.cell_type == "угловая" and y1 > y2:
                if (self.angle == 180 or self.angle == 270) and (other_cell.angle == 90 or other_cell.angle == 270):
                    return True
            if self.cell_type == "угловая" and y1 < y2:
                if (self.angle == 0 or self.angle == 90) and (other_cell.angle == 90 or other_cell.angle == 270):
                    return True
            return False
        if self.cell_type == "прямая" and other_cell.cell_type == "прямая":
            if y1 != y2:
                if (self.angle == 90 or self.angle == 270) and (self.angle + other_cell.angle) % 180 == 0:
                    return True
            if x1 != x2:
                if (self.angle == 0 or self.angle == 180) and (self.angle + other_cell.angle) % 180 == 0:
                    return True
            return False
        if self.cell_type == "конечная" and other_cell.cell_type == "прямая" or self.cell_type == "прямая" and other_cell.cell_type == "конечная":
            if (self.cell_type == "конечная" and (self.angle == 0 or self.angle == 180)) and (self.angle + other_cell.angle) % 180 == 90:
                return True
            if (other_cell.cell_type == "конечная" and (other_cell.angle == 0 or other_cell.angle == 180)) and (self.angle + other_cell.angle) % 180 == 90:
                return True
            return False
        if self.cell_type == "конечная" and other_cell.cell_type == "угловая" or self.cell_type == "угловая" and other_cell.cell_type == "конечная":
            if self.cell_type == "конечная" and x1 < x2:
                if self.angle == 270 and (other_cell.angle == 90 or other_cell.angle == 180):
                    return True
            if self.cell_type == "конечная" and x1 > x2:
                if self.angle == 90 and (other_cell.angle == 0 or other_cell.angle == 270):
                    return True
            if other_cell.cell_type == "конечная" and x1 < x2:
                if other_cell.angle == 90 and (self.angle == 0 or other_cell.angle == 270):
                    return True
            if other_cell.cell_type == "конечная" and x1 > x2:
                if other_cell.angle == 270 and (self.angle == 90 or self.angle == 180):
                    return True
            return False

    @staticmethod
    def propagate_highlight(matrix):
        rows, cols = len(matrix), len(matrix[0])
        queue = [(x, y) for x in range(rows) for y in range(cols) if matrix[x][y].highlighted]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        while queue:
            x, y = queue.pop(0) 
            cell = matrix[x][y]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy 
                if 0 <= nx < rows and 0 <= ny < cols:
                    neighbor = matrix[nx][ny]
                    if not neighbor.highlighted and cell.is_connected(neighbor, x, y, nx, ny):
                        neighbor.highlighted = True 
                        queue.append((nx, ny))
        return matrix
class Labirint():
    def __init__(self):
        pass
    def rightmap(self, param):
        firstend_image = Image.open("/home/alex/python_app/lab5/fourth.jpeg")
        middle_image = Image.open("/home/alex/python_app/lab5/vertical.jpeg")
        startend_image = Image.open("/home/alex/python_app/lab5/right.jpeg")
        cell_size = firstend_image.size
        matr = [[0] * param for _ in range(param)]
        for y in range(param):
            for x in range(param):                                                                                                                                  
                if 0 < y < param -1:
                    matr[x][y] = 90
                elif y == 0:
                    if x % 2 == 1:
                        matr[x][y] = 0
                    else:
                        matr[x][y] = 90
                elif y == param -1:
                    if x % 2 == 1:
                        matr[x][y] = 180
                    else:
                        matr[x][y] = 270
        matr[0][0] = 0
        if param % 2 == 0:
            matr[param-1][0] = 0
        else:
            matr[param-1][param-1] = 180
        field_width = cell_size[0] * len(matr[0])
        field_height = cell_size[1] * len(matr)
        field = Image.new("RGB", (field_width, field_height))

        for i in range(len(matr)):
            for j in range(len(matr[i])):
                if j == 0 or j == len(matr[i]) - 1:
                    img = firstend_image
                else:
                    img = middle_image
                if param % 2 == 0:
                    if j == 0 and (i == 0 or i == param - 1):
                        img = startend_image
                else:
                    if j == 0 and i == 0 or j == param - 1 and i == param - 1:
                        img = startend_image
                rot_image = img.rotate(matr[i][j])
                field.paste(rot_image, (j * cell_size[0], i * cell_size[1]))

        field.save("rightmap.jpeg")

    def rand_rightmap(self, param):
        values = [0, 90, 180, 270]
        matr = [[random.choice(values) for _ in range(param)] for _ in range(param)]
        firstend_image = Image.open("/home/alex/python_app/lab5/fourth.jpeg")
        middle_image = Image.open("/home/alex/python_app/lab5/vertical.jpeg")
        startend_image = Image.open("/home/alex/python_app/lab5/right.jpeg")
        cell_size = firstend_image.size
        field_width = cell_size[0] * len(matr[0])
        field_height = cell_size[1] * len(matr)
        image_matrix = []
        for i in range(len(matr)):
            row_images = []
            for j in range(len(matr[i])):
                if j == 0 or j == len(matr[i]) - 1:
                    img = firstend_image
                else:
                    img = middle_image
                if param % 2 == 0:
                    if j == 0 and (i == 0 or i == param - 1):
                        img = startend_image
                else:
                    if j == 0 and i == 0 or j == param - 1 and i == param - 1:
                        img = startend_image
                rot_image = img.rotate(matr[i][j])
                rot_image.save(f"tile_{i}_{j}.jpeg")
                row_images.append(f"tile_{i}_{j}.jpeg")
            image_matrix.append(row_images)

        return matr, image_matrix, cell_size
        
class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Введите число")
        self.start_time = None
        self.timer_duration = 120000
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.Font(None, 36)
        self.game_over = False
        self.input_number = ""
        self.message = "Введите число от 10 до 100:"
        self.running = True
        self.labirint = Labirint()
        self.param = None
        self.matrix = None
        self.new_matrix = None
        self.images_matrix = None
        self.cell_size = None
        self.image_objects = []

    def draw_text(self, text, x, y):
        render_text = self.FONT.render(text, True, self.BLACK)
        self.screen.blit(render_text, (x, y))

    def create_new_matrix(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        cell_matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                if j == 0 or j == cols -1:
                    cell_type = "угловая"
                else:
                    cell_type = "прямая"
                if j == 0 and i == 0:
                    cell_type = "конечная"
                if cols % 2 == 0:
                    if j == 0 and i == rows -1:
                        cell_type = "конечная"
                if cols % 2 == 1:
                    if j == cols - 1 and i == rows -1:
                        cell_type = "конечная"
                highlighted = (i == 0 and j == 0)
                row.append(Cell(cell_type, self.matrix[i][j], highlighted))
            cell_matrix.append(row)
        return cell_matrix

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_number.isdigit():
                    number = int(self.input_number)
                    if 10 <= number <= 100:
                        self.start_time = pygame.time.get_ticks()
                        self.param = number
                        self.matrix, self.images_matrix, cell_size = self.labirint.rand_rightmap(self.param)
                        self.cell_size = cell_size
                        self.load_images()
                    else:
                        self.message = "Неверный ввод! Попробуйте снова."
                    self.input_number = ""
                else:
                    self.message = "Введите число!"
            elif event.key == pygame.K_BACKSPACE:
                self.input_number = self.input_number[:-1]
            else:
                self.input_number += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // self.cell_size[0], (y-40) // self.cell_size[1]
            if 0 <= row < self.param and 0 <= col < self.param:
                self.matrix[row][col] = (self.matrix[row][col] + 90) % 360
                img = pygame.image.load(self.images_matrix[row][col])
                rotated_img = pygame.transform.rotate(img, self.matrix[row][col])
                self.image_objects[row][col] = pygame.transform.rotate(pygame.image.load(self.images_matrix[row][col]), self.matrix[row][col])
                self.new_matrix = self.create_new_matrix()
                self.new_matrix = Cell.propagate_highlight(self.new_matrix)
                self.image_objects[row][col] = pygame.transform.rotate(
                    pygame.image.load(self.images_matrix[row][col]), self.matrix[row][col]
                )
                if self.param % 2 == 0:
                    winning_row, winning_col = self.param -1, 0
                else:
                    winning_row, winning_col = self.param -1, self.param -1
                if self.new_matrix[winning_row][winning_col].highlighted:
                    self.messange = "Ты выиграл!"
                    self.game_over = True
                pygame.display.flip()

    def load_images(self):
        self.image_objects = [] 
        for i in range(self.param):
            row_images = [] 
            for j in range(self.param):
                img = pygame.image.load(self.images_matrix[i][j]) 
                row_images.append(img) 
            self.image_objects.append(row_images) 
        self.WIDTH = self.cell_size[0] * self.param 
        self.HEIGHT = self.cell_size[1] * self.param + 40 
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_timer(self, remaining_time):
        timer_text = f"Время: {remaining_time} сек."
        timer_surface = self.FONT.render(timer_text, True, self.BLACK)
        timer_rect = pygame.Rect(0, 0, self.WIDTH, 40)
        pygame.draw.rect(self.screen, (220, 220, 220), timer_rect)
        self.screen.blit(timer_surface, (10, 10))

    def run(self):
        while self.running:
            self.screen.fill(self.WHITE)
            if self.game_over and self.messange == "Ты проиграл( Вот правильное решение:":
                self.screen.fill(self.WHITE)
                self.draw_text(self.messange, 50, 50)
                self.labirint.rightmap(self.param)
                solution_image = pygame.image.load("rightmap.jpeg")
                solution_image = pygame.transform.scale(solution_image, (self.WIDTH -75, self.HEIGHT - 150))
                self.screen.blit(solution_image, (50, 100))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.running = False
                continue
            if self.game_over: 
                self.screen.fill(self.WHITE) 
                self.draw_text(self.messange, 50, 50)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.running = False
                continue
            if self.cell_size:
                pygame.draw.rect(self.screen, (255, 255, 0), (0, 40, self.cell_size[0], self.cell_size[1]), 3)
            self.draw_text(self.message, 50, 50)
            self.draw_text(self.input_number, 50, 100)
            if self.image_objects:
                for i in range(self.param):
                    for j in range(self.param):
                        x, y = j * self.cell_size[0], i * self.cell_size[1] + 40
                        self.screen.blit(self.image_objects[i][j], (x, y))
                        if self.new_matrix:
                            if self.new_matrix[i][j].highlighted:
                                pygame.draw.rect(self.screen, (255, 255, 0), (x, y, self.cell_size[0], self.cell_size[1]), 5)
            if self.start_time is not None:
                elapsed_time = pygame.time.get_ticks() - self.start_time
                remaining_time = max(0, (self.timer_duration - elapsed_time) // 1000)
                self.draw_timer(remaining_time)
                if remaining_time == 0:
                    self.messange = "Ты проиграл( Вот правильное решение:"
                    self.game_over = True
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // self.cell_size[0], (y-40) // self.cell_size[1]
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
        pygame.quit()
        sys.exit()

game = Game()
game.run()
