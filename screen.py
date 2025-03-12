#Emulator for a CHIP-8 system using Python
#This file creates the window using pygame

#Importing all required modules

import pygame
import emulator

#Pygame setup
pygame.init()
SCALE = 10
screen = pygame.display.set_mode((64 * SCALE, 32 * SCALE))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("CHIP-8")
chip8 = emulator.Chip8()

#Loading the ROM file
try:
    chip8.load_ROM("testrom.ch8")
except FileNotFoundError:
    print("File not found")
    running = False


#Keymap for chip8
keymap = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF,
}

#Loop for running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in keymap:
                chip8.keypad[keymap[event.key]] = 1
        
        elif event.type == pygame.KEYUP:
            if event.key in keymap:
                chip8.keypad[keymap[event.key]] = 0
    
    

    opcode = emulator.fetch_code(chip8)
    emulator.decode_and_execute(chip8, opcode)


    chip8.update_timer()

    
    chip8.draw(screen)
    clock.tick(60)

pygame.quit()