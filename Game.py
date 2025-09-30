import pygame
import serial
import time


ser = serial.Serial('COM3', 9600) 
time.sleep(2)  


pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MPU6050 Tilt Game (LED-based)")


char_size = 40
x, y = WIDTH // 2, HEIGHT // 2
angle = 0  
speed = 10

clock = pygame.time.Clock()
running = True


char_surface = pygame.Surface((char_size, char_size))
char_surface.fill((0, 200, 100))

while running:
    clock.tick(30)
    win.fill((20, 20, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
       
        line = ser.readline().decode('utf-8').strip()
        print("Arduino:", line)  

        if "Pitch front detected" in line:
            y -= speed
        elif "Pitch back detected" in line:
            y += speed
        elif "Roll Right Detected" in line:
            x += speed
            angle -= 10 
        elif "Roll Left Detected" in line:
            x -= speed
            angle += 10  


        x = max(0, min(WIDTH - char_size, x))
        y = max(0, min(HEIGHT - char_size, y))

    except Exception as e:
        print("Error:", e)


    rotated_char = pygame.transform.rotate(char_surface, angle)
    rect = rotated_char.get_rect(center=(x + char_size // 2, y + char_size // 2))

 
    win.blit(rotated_char, rect.topleft)
    pygame.display.update()

ser.close()
pygame.quit()
