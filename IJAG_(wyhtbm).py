import pygame
import sqlite3
import random
import os
import sys

clear = lambda: os.system('cls')

def handle_error(type, value, traceback):
    print("I am a bad coder)")
    print(f"{type} error has occurred, the value: {value}, and you can see traceback: {traceback}")
    input()
    
sys.excepthook = handle_error

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    up, down, left, right = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.rect.x -= 5
        if keys[self.right]:
            self.rect.x += 5
        if keys[self.up]:
            self.rect.y -= 5
        if keys[self.down]:
            self.rect.y += 5

class Game:
    def __init__(self):
        self.num = 5
        self.SPEED = 5000
        self.score = 0
        self.yellow_circles = []
        self.red_triangles = []
        self.conn = sqlite3.connect('game.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players
                     (name TEXT, points INT)''')

    def create_new_yellow_circle(self):
        x = random.randint(20, 1900)
        y = random.randint(20, 1050)
        
        yellow_circle = pygame.Rect(x, y, 10, 10)
        self.yellow_circles.append(yellow_circle)

    def create_new_red_triangle(self):
        x = random.randint(20, 1900)
        y = random.randint(20, 1050)
        red_triangle = pygame.Rect(x, y, 20, 20)
        self.red_triangles.append(red_triangle)

    def run(self):
        running = True
        pygame.init()
        self.size = (1920, 1080)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Игра на Pygame")
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(300, 300)
        self.all_sprites.add(self.player)
        clock = pygame.time.Clock()
        last_red_triangle_update = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.all_sprites.update()
            self.screen.fill(BLACK)
            
            for yellow_circle in self.yellow_circles:
                pygame.draw.circle(self.screen, (255, 255, 0), (yellow_circle.x + 5, yellow_circle.y + 5), 5)

                if self.player.rect.colliderect(yellow_circle):
                    if self.SPEED == 5000:
                        self.score += 1
                    elif self.SPEED == 3500:
                        self.score += 2
                    elif self.SPEED == 1500:
                        self.score += 3
                    self.yellow_circles.remove(yellow_circle)
                    if self.score >= 100:
                        running = False

            for red_triangle in self.red_triangles:
                pygame.draw.polygon(self.screen, (255, 0, 0), [(red_triangle.x, red_triangle.y + 20), (red_triangle.x + 10, red_triangle.y), (red_triangle.x + 20, red_triangle.y + 20)])

                if self.player.rect.colliderect(red_triangle):
                    running = False

            current_time = pygame.time.get_ticks()
            if current_time - last_red_triangle_update > self.SPEED:
                for red_triangle in self.red_triangles:
                    red_triangle.x = random.randint(20, 1900)
                    red_triangle.y = random.randint(20, 1050)
                last_red_triangle_update = current_time

            while len(self.yellow_circles) < 25:
                self.create_new_yellow_circle()

            while len(self.red_triangles) < self.num:
                self.create_new_red_triangle()
                
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        if self.score >= 100:
            text = font.render('You win! Congrats!', True, (255, 255, 255))
            text_rect = text.get_rect(center=(960, 540))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            self.save_score(player_name, self.score)
            pygame.time.wait(4000)
        else:
            text = font.render('Game Over!', True, (255, 255, 255))
            text_rect = text.get_rect(center=(960, 540))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(4000)
        pygame.quit()
        clear()
        self.main_menu()

    def save_score(self, player_name, score):
        self.cursor.execute("INSERT INTO players (name, points) VALUES (?, ?)", (player_name, score))
        self.conn.commit()

    def show_top_scores(self):
        top_scores = self.cursor.execute("SELECT name, points FROM players ORDER BY points DESC LIMIT 5").fetchall()
        for i, (name, points) in enumerate(top_scores, 1):
            print(f"{i}. {name}: {points} points")

    def main_menu(self):
        print("Главное меню")
        print("1. Настройки")
        print("2. Играть")
        print("3. Показать топ-5 игроков")
        print("4. Правила")
        print("5. Выход")

        choice = input("Выберите пункт меню: ")
        if choice == "1":
            clear()
            print("Настройки управления")
            print("1. Изменить клавиши")
            print("2. Изменить сложность")
            print("3. Назад")
            choice = input("Выберите пункт настройки: ")
            if choice == '1':
                clear()
                print("Текущие клавиши управления:")
                print("Вверх:", pygame.key.name(pygame.K_UP))
                print("Вниз:", pygame.key.name(pygame.K_DOWN))
                print("Влево:", pygame.key.name(pygame.K_LEFT))
                print("Вправо:", pygame.key.name(pygame.K_RIGHT))

                new_up = input("Введите новую клавишу для движения вверх: ")
                new_down = input("Введите новую клавишу для движения вниз: ")
                new_left = input("Введите новую клавишу для движения влево: ")
                new_right = input("Введите новую клавишу для движения вправо: ")

                Player.up = getattr(pygame, f"K_{new_up.lower()}")
                Player.down = getattr(pygame, f"K_{new_down.lower()}")
                Player.left = getattr(pygame, f"K_{new_left.lower()}")
                Player.right = getattr(pygame, f"K_{new_right.lower()}")
                print("Клавиши управления успешно обновлены!")
                input("Нажмите enter чтобы назад")
                clear()
                self.main_menu()

            elif choice == '2':
                clear()
                print('Текущая сложность: 1')
                new_diff = input('Введите новую сложность (1, 2, 3): ')
                if new_diff == '1':
                    self.SPEED = 5000
                    self.num = 10
                elif new_diff == '2':
                    self.SPEED = 3500
                    self.num = 15
                elif new_diff == '3':
                    self.SPEED = 1500
                    self.num = 20
                print("Сложность изменена успешно!")
                print("Текущая сложность:", new_diff)
                input("Нажмите enter чтобы назад")
                clear()
                self.main_menu()
            
            else:
                self.main_menu()
                
        elif choice == '2':
            self.run()
            self.conn.close()
        elif choice == '3':
            clear()
            self.show_top_scores()
            print("Нажмите enter чтобы вернуться")
            print("Enter pass for clearing database")
            h = input()
            if h == "/clear_data":
                self.cursor.execute("DELETE FROM players;")
                self.conn.commit()
            clear()
            self.main_menu()
        elif choice == '4':
            print("Правила игры:")
            print("1) Собирайте жёлтые кружки.")
            print("За каждый кружок вы получаете 1/2/3 поинта в зависимости от сложности")
            print("2) Остерегайтесь красных треугольников!")
            print("3) Наберите 100 очков")
            print("На этом всё) Удачи!")
            input("Нажмите enter чтобы назад")
            clear()
            self.main_menu()
        elif choice == '5':
            self.conn.close()
            sys.exit()
        else:
            print("An error occured: Invalid InputData Type!")
            input("Press enter to continue")
            clear()
            self.main_menu()

clear()
player_name = input("Введите ваше имя: ")
game_instance = Game()
game_instance.main_menu()
