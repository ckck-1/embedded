import pygame
import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)

pygame.init()
pygame.mixer.init()
move_sound = pygame.mixer.Sound("move.wav")
win_sound = pygame.mixer.Sound("win.wav")
switch_sound = pygame.mixer.Sound("switch.wav")

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MPU6050 Tilt Game Full Version")

char_size = 40
x, y = WIDTH // 2, HEIGHT // 2
angle = 0
speed = 10
moving = False

goal_rect = pygame.Rect(WIDTH-50, HEIGHT-50, 50, 50)

clock = pygame.time.Clock()
running = True

char_surface = pygame.Surface((char_size, char_size))
char_surface.fill((0, 200, 100))

while running:
    clock.tick(30)
    win.fill((20, 20, 30))
    moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode('utf-8').strip()

        if "Pitch front detected" in line:
            y -= speed
            moving = True
            move_sound.play()
        elif "Pitch back detected" in line:
            y += speed
            moving = True
            move_sound.play()
        if "Roll Right Detected" in line:
            x += speed
            angle -= 10
            moving = True
            move_sound.play()
        elif "Roll Left Detected" in line:
            x -= speed
            angle += 10
            moving = True
            move_sound.play()
        if "Switch Pressed" in line:
            switch_sound.play()
            char_surface.fill((200, 0, 200))

        if "No Pitch and No Roll" in line:
            char_surface.fill((0, 200, 100))

        x = max(0, min(WIDTH - char_size, x))
        y = max(0, min(HEIGHT - char_size, y))

    except:
        pass

    rotated_char = pygame.transform.rotate(char_surface, angle)
    rect = rotated_char.get_rect(center=(x + char_size // 2, y + char_size // 2))
    win.blit(rotated_char, rect.topleft)

    pygame.draw.rect(win, (255, 255, 0), goal_rect)
    char_rect = pygame.Rect(x, y, char_size, char_size)
    if char_rect.colliderect(goal_rect):
        win_sound.play()
        print("You Win!")
        running = False

    pygame.display.update()

ser.close()
pygame.quit()
