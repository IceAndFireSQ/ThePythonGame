import pygame
import os
from game import Game

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    game_instance = Game()
    game_instance.main_menu()
    game_instance.conn.close()

if __name__ == "__main__":
    main()
