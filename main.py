import random
import pygame
from pygame.locals import *
import hand
import threading
import queue
import pygame_gui

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

    #place where car starts
    lanes = [150, 250, 350, 450]

    #start game
    start = 0
    game_over = 0

    # Menedżer GUI
    gui_manager = pygame_gui.UIManager((width, height))

    # Przycisk resetowania gry
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width - 150) // 2, (height - 50) // 2, 150, 50),
        text="Reset",
        manager=gui_manager
    )



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

        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if (event.type == QUIT or event.type == ord('q')):
                running = 0
            gui_manager.process_events(event)


        #przekazanie wartości z wątku hand_loop
        while not hand_queue.empty():
            value = hand_queue.get()
            #sterownie pojazdem
            player.rect.x = 100 + value*1/2

            start = 1


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




        # drow the other car
        if len(vehicle_group) < 4:

            # ensure there's enough gap between vehicles
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False

            if add_vehicle:
                lane = random.choice(lanes)
                image = pygame.image.load('C:/Users/nosal/PycharmProjects/car_hand_game/taxi.png')
                vehicle = Vehicle(image, lane, 40)
                vehicle_group.add(vehicle)

        # move a vehicle
        if start==1 and game_over == 0:
            for vehicle in vehicle_group:
                vehicle.rect.y += speed

                # Kolizja z pojazdem
                if player.rect.colliderect(vehicle.rect):
                    game_over = True

                # remove vehicle once it goes off screen
                if vehicle.rect.top >= height:
                    vehicle.kill()
                    # add to score
                    score += 1
                    # speed up the game after passing 5 vehicles
                    if score > 0 and score % 5 == 0:
                        speed += 0.5

        # drow the car
        player_group.draw(screen)
        vehicle_group.draw(screen)

        # Czcionka tekstu
        font = pygame.font.Font(None, 36)
        # Tworzenie napisu
        text = font.render(f"score:{score}", True, (255, 255, 255))
        # Pozycja napisu (górny prawy róg)
        text_rect = text.get_rect(topright=(width - 10, 10))

        # Rysowanie napisu na ekranie
        screen.blit(text, text_rect)

        #game over
        if game_over:
            screen.fill((0, 0, 0))  # Czarne tło

            # Wyświetlenie przycisku resetu
            gui_manager.update(time_delta)
            gui_manager.draw_ui(screen)

            # Czcionka tekstu
            font = pygame.font.Font(None, 36)
            # Tworzenie napisu
            text1 = font.render(f"GAME OVER", True, (255, 255, 255))
            text2 = font.render(f"your score: {score}", True, (255, 255, 255))
            # Pozycja napisu (górny prawy róg)
            text_rect1 = text.get_rect(center=(width/2-30, 50))
            text_rect2 = text.get_rect(center=(width/2-30, 70))

            # Rysowanie napisu na ekranie
            screen.blit(text1, text_rect1)
            screen.blit(text2, text_rect2)

            # Sprawdzenie kliknięcia przycisku resetu
            if reset_button.check_pressed():
                game_over = False
                # Przywróć stan gry do początkowego
                player.rect.x = player_x
                player.rect.y = player_y
                vehicle_group.empty()
                score = 0
                speed = 2





        # Aktualizacja wyświetlania GUI
        gui_manager.update(time_delta)
        gui_manager.draw_ui(screen)

        # Wyświetlanie przycisku resetu tylko po przegranej
        if game_over:
            reset_button.show()
        else:
            reset_button.hide()

        pygame.display.flip()

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

