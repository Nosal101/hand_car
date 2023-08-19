import random
import pygame
from pygame.locals import *
import hand
import threading
import queue

pygame.init()


def game_loop():
    # screen
    width = 600
    height = 600
    screen_size = (width, height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Car Game")
    # colors
    gray = (100, 100, 100)
    green = (76, 200, 55)
    white = (255, 255, 255)
    # game stats
    gameover = 0
    speed = 2
    score = 0
    # game loop
    clock = pygame.time.Clock()
    fps = 120

    # player's starting coordinates
    player_x = 250
    player_y = 400

    # every class
    class Vehicle(pygame.sprite.Sprite):

        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            image_scale = 45 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

    class PlayerVehicle(Vehicle):

        def __init__(self, x, y):
            image = pygame.image.load('C:/Users/nosal/PycharmProjects/car_hand_game/car.png')
            super().__init__(image, x, y)

    # tworzenie obiektów
    player_group = pygame.sprite.Group()
    vehicle_group = pygame.sprite.Group()
    player = PlayerVehicle(player_x, player_y)
    player_group.add(player)

    running = True

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if (event.type == QUIT or event.type == ord('q')):
                running = 0

        #przekazanie wartości z wątku hand_loop
        while not hand_queue.empty():
            value = hand_queue.get()
            #sterownie pojazdem
            player.rect.x = 100 + value*1/2

        # draw the grass
        screen.fill(green)
        # drow the street
        pygame.draw.rect(screen, gray, pygame.Rect(100, 0, width - 200, height))
        # drow the stripe
        pygame.draw.rect(screen, white, pygame.Rect(100, 0, 5, height))
        pygame.draw.rect(screen, white, pygame.Rect(195, 0, 10, height))
        pygame.draw.rect(screen, white, pygame.Rect(295, 0, 10, height))
        pygame.draw.rect(screen, white, pygame.Rect(395, 0, 10, height))
        pygame.draw.rect(screen, white, pygame.Rect(500 - 5, 0, 5, height))
        for i in range(1, 14, 2):
            pygame.draw.rect(screen, gray, pygame.Rect(150, 40 * i, width - 300, 30))
        # drow the car
        player_group.draw(screen)

        # screen update
        pygame.display.update()
def hand_loop():
    # open the hand project
    for value in hand.control():
        hand_queue.put(value)


# Uruchomienie wątku obsługującego grę
game_thread = threading.Thread(target=game_loop)
hand_queue = queue.Queue()
hand_thread = threading.Thread(target=hand_loop, args=(hand_queue,))
game_thread.start()

# Uruchomienie wątku obsługującego wykrywanie dłoni
hand_thread = threading.Thread(target=hand_loop)
hand_thread.start()

# Zakończenie wątków po zakończeniu gry
game_thread.join()
hand_thread.join()


pygame.quit()

